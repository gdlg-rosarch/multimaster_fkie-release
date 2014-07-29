Name:           ros-hydro-multimaster-msgs-fkie
Version:        0.3.13
Release:        0%{?dist}
Summary:        ROS multimaster_msgs_fkie package

Group:          Development/Libraries
License:        BSD
URL:            http://ros.org/wiki/multimaster_msgs_fkie
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-hydro-message-runtime
Requires:       ros-hydro-std-msgs
BuildRequires:  ros-hydro-catkin
BuildRequires:  ros-hydro-message-generation
BuildRequires:  ros-hydro-std-msgs

%description
The messages required by multimaster packages.

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/hydro/setup.sh" ]; then . "/opt/ros/hydro/setup.sh"; fi
mkdir -p build && cd build
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
cd build
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/hydro

%changelog
* Tue Jul 29 2014 Alexander Tiderko <alexander.tiderko@gmail.com> - 0.3.13-0
- Autogenerated by Bloom

