"""dVRK console controls using dvrk_python."""

from __future__ import annotations

import argparse

import crtk
import dvrk
from python_qt_binding import QtCore, QtWidgets
from rqt_gui_py.plugin import Plugin
from rqt_crtk.ral_executor import QtRALExecutor


class ConsolePlugin(Plugin):
    def __init__(self, context):
        super().__init__(context)
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--console", default="console")
        options, unknown = parser.parse_known_args(context.argv())
        if unknown:
            raise ValueError("unknown plugin arguments: {}".format(" ".join(unknown)))
        self._ral = crtk.ral("rqt_dvrk_console")
        self._console = dvrk.console(self._ral, options.console)
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        buttons = QtWidgets.QHBoxLayout()
        start = QtWidgets.QPushButton("Start teleoperation")
        start.clicked.connect(self._console.teleop_start)
        stop = QtWidgets.QPushButton("Stop teleoperation")
        stop.clicked.connect(self._console.teleop_stop)
        buttons.addWidget(start)
        buttons.addWidget(stop)
        layout.addLayout(buttons)
        scale = QtWidgets.QDoubleSpinBox()
        scale.setRange(0.0, 10.0)
        scale.setSingleStep(0.1)
        apply_scale = QtWidgets.QPushButton("Set teleoperation scale")
        apply_scale.clicked.connect(lambda: self._console.teleop_set_scale(scale.value()))
        layout.addWidget(scale)
        layout.addWidget(apply_scale)
        selection = QtWidgets.QHBoxLayout()
        self._teleop_name = QtWidgets.QLineEdit()
        self._teleop_name.setPlaceholderText("teleoperation component name")
        select = QtWidgets.QPushButton("Select")
        select.clicked.connect(self._select)
        unselect = QtWidgets.QPushButton("Unselect")
        unselect.clicked.connect(self._unselect)
        selection.addWidget(self._teleop_name)
        selection.addWidget(select)
        selection.addWidget(unselect)
        layout.addLayout(selection)
        self._status = QtWidgets.QLabel()
        layout.addWidget(self._status)
        layout.addStretch()
        self._widget = widget
        context.add_widget(widget)
        self._executor = QtRALExecutor(self._ral)
        self._spin_timer = QtCore.QTimer(widget)
        self._spin_timer.timeout.connect(self._executor.spin_once)
        self._spin_timer.start(10)
        self._timer = QtCore.QTimer(widget)
        self._timer.timeout.connect(self._update_status)
        self._timer.start(250)

    def _select(self):
        name = self._teleop_name.text().strip()
        if name:
            self._console.teleop_select(name)

    def _unselect(self):
        name = self._teleop_name.text().strip()
        if name:
            self._console.teleop_unselect(name)

    def _update_status(self):
        name = self._teleop_name.text().strip()
        selection = (
            "; {}: {}".format(name, "selected" if self._console.teleop_is_selected(name) else "not selected")
            if name else ""
        )
        self._status.setText(
            "Current teleoperation scale: {:.2f}{}".format(
                self._console.teleop_get_scale(), selection
            )
        )

    def shutdown_plugin(self):
        self._timer.stop()
        self._spin_timer.stop()
        self._executor.shutdown()
