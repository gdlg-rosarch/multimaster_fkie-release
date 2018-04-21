# Script generated with Bloom
pkgdesc="ROS - Synchronize the local ROS master to the remote masters discovered by master_discovery_fkie node. The registration of topics and services is only perform by local ROS master."
url='http://ros.org/wiki/master_sync_fkie'

pkgname='ros-kinetic-master-sync-fkie'
pkgver='0.7.8_1'
pkgrel=1
arch=('any')
license=('BSD'
)

makedepends=('ros-kinetic-catkin'
'ros-kinetic-master-discovery-fkie'
'ros-kinetic-multimaster-msgs-fkie'
)

depends=('ros-kinetic-master-discovery-fkie'
'ros-kinetic-multimaster-msgs-fkie'
'ros-kinetic-rosgraph'
'ros-kinetic-roslib'
'ros-kinetic-rospy'
)

conflicts=()
replaces=()

_dir=master_sync_fkie
source=()
md5sums=()

prepare() {
    cp -R $startdir/master_sync_fkie $srcdir/master_sync_fkie
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

