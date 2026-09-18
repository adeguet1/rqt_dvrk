from setuptools import find_packages, setup

setup(name="rqt_dvrk", version="0.1.0", packages=find_packages(exclude=["test"]),
      data_files=[("share/ament_index/resource_index/packages", ["resource/rqt_dvrk"]),
                  ("share/ament_index/resource_index/rqt_gui__pluginlib__plugin",
                   ["resource/rqt_gui__pluginlib__plugin/rqt_dvrk"]),
                  ("share/rqt_dvrk", ["package.xml", "plugin.xml"])],
      install_requires=["setuptools"], zip_safe=True,
      maintainer="dVRK maintainers", maintainer_email="support@intusurg.com",
      description="dVRK-specific ROS 2 rqt plugins.", license="BSD-3-Clause")
