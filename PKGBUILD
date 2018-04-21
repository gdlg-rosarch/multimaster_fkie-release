# Script generated with Bloom
pkgdesc="ROS - The configuration node loads a given launch configuration and offers services to list or start the contained nodes. It provides additional description extracted from launch file. This is used by node_manager_fkie."
url='http://ros.org/wiki/default_cfg_fkie'

pkgname='ros-kinetic-default-cfg-fkie'
pkgver='0.7.8_1'
pkgrel=1
arch=('any')
license=('BSD'
)

makedepends=('ros-kinetic-catkin'
'ros-kinetic-multimaster-msgs-fkie'
)

depends=('ros-kinetic-multimaster-msgs-fkie'
'ros-kinetic-roslaunch'
'ros-kinetic-roslib'
'ros-kinetic-rospy'
)

conflicts=()
replaces=()

_dir=default_cfg_fkie
source=()
md5sums=()

prepare() {
    cp -R $startdir/default_cfg_fkie $srcdir/default_cfg_fkie
}

build() {
  # Use ROS environment variables
  source /usr/share/ros-build-tools/clear-ros-env.sh
  [ -f /opt/ros/kinetic/setup.bash ] && source /opt/ros/kinetic/setup.bash

  # Create build directory
  [ -d ${srcdir}/build ] || mkdir ${srcdir}/build
  cd ${srcdir}/build

  # Fix Python2/Python3 conflicts
  /usr/share/ros-build-tools/fix-python-scripts.sh -v 2 ${srcdir}/${_dir}

  # Build project
  cmake ${srcdir}/${_dir} \
        -DCMAKE_BUILD_TYPE=Release \
        -DCATKIN_BUILD_BINARY_PACKAGE=ON \
        -DCMAKE_INSTALL_PREFIX=/opt/ros/kinetic \
        -DPYTHON_EXECUTABLE=/usr/bin/python2 \
        -DPYTHON_INCLUDE_DIR=/usr/include/python2.7 \
        -DPYTHON_LIBRARY=/usr/lib/libpython2.7.so \
        -DPYTHON_BASENAME=-python2.7 \
        -DSETUPTOOLS_DEB_LAYOUT=OFF
  make
}

package() {
  cd "${srcdir}/build"
  make DESTDIR="${pkgdir}/" install
}

