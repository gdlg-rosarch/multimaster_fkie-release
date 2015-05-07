Name:           ros-jade-node-manager-fkie
Version:        0.4.1
Release:        0%{?dist}
Summary:        ROS node_manager_fkie package

Group:          Development/Libraries
License:        BSD, some icons are licensed under the GNU Lesser General Public License (LGPL) or Creative Commons Attribution-Noncommercial 3.0 License
URL:            http://ros.org/wiki/node_manager_fkie
Source0:        %{name}-%{version}.tar.gz

Requires:       python-docutils
Requires:       python-paramiko
Requires:       ros-jade-default-cfg-fkie
Requires:       ros-jade-dynamic-reconfigure
Requires:       ros-jade-master-discovery-fkie
Requires:       ros-jade-master-sync-fkie
Requires:       ros-jade-multimaster-msgs-fkie
Requires:       ros-jade-python-qt-binding
Requires:       ros-jade-rosgraph
Requires:       ros-jade-roslaunch
Requires:       ros-jade-roslib
Requires:       ros-jade-rosmsg
Requires:       ros-jade-rospy
Requires:       ros-jade-rosservice
Requires:       ros-jade-rqt-gui
Requires:       ros-jade-rqt-reconfigure
Requires:       screen
Requires:       xterm
BuildRequires:  ros-jade-catkin
BuildRequires:  ros-jade-master-discovery-fkie
BuildRequires:  ros-jade-multimaster-msgs-fkie

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
if [ -f "/opt/ros/jade/setup.sh" ]; then . "/opt/ros/jade/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/jade" \
        -DCMAKE_PREFIX_PATH="/opt/ros/jade" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jade/setup.sh" ]; then . "/opt/ros/jade/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/jade

%changelog
* Thu May 07 2015 Alexander Tiderko <alexander.tiderko@gmail.com> - 0.4.1-0
- Autogenerated by Bloom

