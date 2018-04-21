# Script generated with Bloom
pkgdesc="ROS - Discover the running ROS Masters in local network. The discovering is done by sending an echo heartbeat messages to a defined multicast group. The alternative is to use a zeroconf/avahi daemon to register the ROS master as service and discover other ROS masters."
url='http://ros.org/wiki/master_discovery_fkie'

pkgname='ros-kinetic-master-discovery-fkie'
pkgver='0.7.8_1'
pkgrel=1
arch=('any')
license=('BSD'
)

makedepends=('ros-kinetic-catkin'
'ros-kinetic-multimaster-msgs-fkie'
'ros-kinetic-std-srvs'
)

depends=('avahi'
'ros-kinetic-multimaster-msgs-fkie'
'ros-kinetic-rosgraph'
'ros-kinetic-roslib'
'ros-kinetic-rospy'
'ros-kinetic-std-srvs'
)

conflicts=()
replaces=()

_dir=master_discovery_fkie
source=()
md5sums=()

prepare() {
    cp -R $startdir/master_discovery_fkie $srcdir/master_discovery_fkie
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

