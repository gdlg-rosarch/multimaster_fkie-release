Name:           ros-hydro-node-manager-fkie
Version:        0.4.0
Release:        0%{?dist}
Summary:        ROS node_manager_fkie package

Group:          Development/Libraries
License:        BSD, some icons are licensed under the GNU Lesser General Public License (LGPL) or Creative Commons Attribution-Noncommercial 3.0 License
URL:            http://ros.org/wiki/node_manager_fkie
Source0:        %{name}-%{version}.tar.gz

Requires:       python-docutils
Requires:       python-paramiko
Requires:       ros-hydro-default-cfg-fkie
Requires:       ros-hydro-dynamic-reconfigure
Requires:       ros-hydro-master-discovery-fkie
Requires:       ros-hydro-master-sync-fkie
Requires:       ros-hydro-multimaster-msgs-fkie
Requires:       ros-hydro-python-qt-binding
Requires:       ros-hydro-rosgraph
Requires:       ros-hydro-roslaunch
Requires:       ros-hydro-roslib
Requires:       ros-hydro-rosmsg
Requires:       ros-hydro-rospy
Requires:       ros-hydro-rosservice
Requires:       ros-hydro-rqt-gui
Requires:       ros-hydro-rqt-reconfigure
Requires:       screen
Requires:       xterm
BuildRequires:  ros-hydro-catkin
BuildRequires:  ros-hydro-master-discovery-fkie
BuildRequires:  ros-hydro-multimaster-msgs-fkie

%description
Graphical interface, written in PySide, to manage the running and configured ROS
nodes on different hosts. For discovering the running ROS master
master_discovery node will be used.

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/hydro/setup.sh" ]; then . "/opt/ros/hydro/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/hydro" \
        -DCMAKE_PREFIX_PATH="/opt/ros/hydro" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/hydro/setup.sh" ]; then . "/opt/ros/hydro/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/hydro

%changelog
* Wed Feb 25 2015 Alexander Tiderko <alexander.tiderko@gmail.com> - 0.4.0-0
- Autogenerated by Bloom

* Thu Jan 22 2015 Alexander Tiderko <alexander.tiderko@gmail.com> - 0.3.17-0
- Autogenerated by Bloom

* Fri Dec 12 2014 Alexander Tiderko <alexander.tiderko@gmail.com> - 0.3.16-0
- Autogenerated by Bloom

* Wed Dec 03 2014 Alexander Tiderko <alexander.tiderko@gmail.com> - 0.3.15-0
- Autogenerated by Bloom

* Fri Oct 24 2014 Alexander Tiderko <alexander.tiderko@gmail.com> - 0.3.14-0
- Autogenerated by Bloom

* Tue Jul 29 2014 Alexander Tiderko <alexander.tiderko@gmail.com> - 0.3.13-0
- Autogenerated by Bloom

