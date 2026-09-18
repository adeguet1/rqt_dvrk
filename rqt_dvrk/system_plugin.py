"""dVRK system power and homing controls using dvrk_python."""

from __future__ import annotations

import argparse

import crtk
import dvrk
from python_qt_binding import QtCore, QtWidgets
from rqt_gui_py.plugin import Plugin
from rqt_crtk.ral_executor import QtRALExecutor


class SystemPlugin(Plugin):
    def __init__(self, context):
        super().__init__(context)
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--system", default="system")
        options, unknown = parser.parse_known_args(context.argv())
        if unknown:
            raise ValueError("unknown plugin arguments: {}".format(" ".join(unknown)))
        self._ral = crtk.ral("rqt_dvrk_system")
        self._system = dvrk.system(self._ral, options.system)
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        home = QtWidgets.QPushButton("Home system")
        home.clicked.connect(lambda: self._confirm("Home the complete system?", self._system.home))
        power_on = QtWidgets.QPushButton("Power on")
        power_on.clicked.connect(self._system.power_on)
        power_off = QtWidgets.QPushButton("Power off")
        power_off.clicked.connect(lambda: self._confirm("Power off the complete system?", self._system.power_off))
        layout.addWidget(home)
        layout.addWidget(power_on)
        layout.addWidget(power_off)
        sound = QtWidgets.QHBoxLayout()
        self._beep_duration = QtWidgets.QDoubleSpinBox()
        self._beep_duration.setRange(0.01, 10.0)
        self._beep_duration.setValue(0.1)
        self._beep_frequency = QtWidgets.QSpinBox()
        self._beep_frequency.setRange(50, 5000)
        self._beep_frequency.setValue(440)
        beep = QtWidgets.QPushButton("Beep")
        beep.clicked.connect(lambda: self._system.beep(
            self._beep_duration.value(), self._beep_frequency.value()
        ))
        sound.addWidget(QtWidgets.QLabel("Duration (s)"))
        sound.addWidget(self._beep_duration)
        sound.addWidget(QtWidgets.QLabel("Hz"))
        sound.addWidget(self._beep_frequency)
        sound.addWidget(beep)
        layout.addLayout(sound)
        speech = QtWidgets.QHBoxLayout()
        self._speech = QtWidgets.QLineEdit()
        self._speech.setPlaceholderText("Text to speak")
        speak = QtWidgets.QPushButton("Speak")
        speak.clicked.connect(self._speak)
        speech.addWidget(self._speech)
        speech.addWidget(speak)
        layout.addLayout(speech)
        layout.addStretch()
        self._widget = widget
        context.add_widget(widget)
        self._executor = QtRALExecutor(self._ral)
        self._spin_timer = QtCore.QTimer(widget)
        self._spin_timer.timeout.connect(self._executor.spin_once)
        self._spin_timer.start(10)

    def _confirm(self, prompt, callback):
        answer = QtWidgets.QMessageBox.question(
            self._widget, "Confirm dVRK command", prompt,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )
        if answer == QtWidgets.QMessageBox.Yes:
            callback()

    def _speak(self):
        text = self._speech.text().strip()
        if text:
            self._system.string_to_speech(text)

    def shutdown_plugin(self):
        self._spin_timer.stop()
        self._executor.shutdown()
