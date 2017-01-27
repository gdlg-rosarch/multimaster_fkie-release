Name:           ros-kinetic-multimaster-fkie
Version:        0.7.2
Release:        0%{?dist}
Summary:        ROS multimaster_fkie package

Group:          Development/Libraries
License:        BSD
URL:            http://ros.org/wiki/multimaster_fkie
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       ros-kinetic-default-cfg-fkie
Requires:       ros-kinetic-master-discovery-fkie
Requires:       ros-kinetic-master-sync-fkie
Requires:       ros-kinetic-multimaster-msgs-fkie
Requires:       ros-kinetic-node-manager-fkie
BuildRequires:  ros-kinetic-catkin

%description
The metapackage to combine the nodes required to establish and manage a
multimaster network. This requires no or minimal configuration. The changes are
automatically detected and synchronized.

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/kinetic/setup.sh" ]; then . "/opt/ros/kinetic/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_LIBDIR="lib" \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/kinetic" \
        -DCMAKE_PREFIX_PATH="/opt/ros/kinetic" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/kinetic/setup.sh" ]; then . "/opt/ros/kinetic/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/kinetic

%changelog
* Fri Jan 27 2017 Alexander Tiderko <alexander.tiderko@gmail.com> - 0.7.2-0
- Autogenerated by Bloom

* Tue Jan 10 2017 Alexander Tiderko <alexander.tiderko@gmail.com> - 0.7.0-0
- Autogenerated by Bloom

* Tue Nov 15 2016 Alexander Tiderko <alexander.tiderko@gmail.com> - 0.6.2-0
- Autogenerated by Bloom

* Tue Oct 18 2016 Alexander Tiderko <alexander.tiderko@gmail.com> - 0.6.1-0
- Autogenerated by Bloom

* Wed Oct 12 2016 Alexander Tiderko <alexander.tiderko@gmail.com> - 0.6.0-0
- Autogenerated by Bloom

* Sat Sep 10 2016 Alexander Tiderko <alexander.tiderko@gmail.com> - 0.5.8-0
- Autogenerated by Bloom

* Wed Sep 07 2016 Alexander Tiderko <alexander.tiderko@gmail.com> - 0.5.7-0
- Autogenerated by Bloom

* Thu Sep 01 2016 Alexander Tiderko <alexander.tiderko@gmail.com> - 0.5.6-0
- Autogenerated by Bloom

* Tue Aug 30 2016 Alexander Tiderko <alexander.tiderko@gmail.com> - 0.5.5-0
- Autogenerated by Bloom

