# rqt_dvrk

dVRK-specific ROS 2 rqt plugins, using PyQt5 through `python_qt_binding`.
Unlike `rqt_crtk`, this package depends on `dvrk_python` because console and
system are dVRK concepts.

```bash
rqt --standalone rqt_dvrk/Console
rqt --standalone rqt_dvrk/System
```

Use `--console NAME` or `--system NAME` when the dVRK namespaces differ from
the defaults.

For a Classic model cart, first start:

```bash
ros2 launch dvrk_model patient_cart.launch.py generation:=Classic
```

Then start the System and Console panels in separate terminals. `Home system`
and `Power off` deliberately require confirmation. Use the Console panel to
start/stop teleoperation, set scale, and select a teleoperation component.
