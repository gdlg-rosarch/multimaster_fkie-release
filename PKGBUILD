# Script generated with Bloom
pkgdesc="ROS - Graphical interface, written in PySide, to manage the running and configured ROS nodes on different hosts. For discovering the running ROS master master_discovery node will be used."
url='http://ros.org/wiki/node_manager_fkie'

pkgname='ros-kinetic-node-manager-fkie'
pkgver='0.7.8_1'
pkgrel=1
arch=('any')
license=('BSD, some icons are licensed under the GNU Lesser General Public License (LGPL) or Creative Commons Attribution-Noncommercial 3.0 License'
)

makedepends=('ros-kinetic-catkin'
'ros-kinetic-diagnostic-msgs'
'ros-kinetic-master-discovery-fkie'
'ros-kinetic-multimaster-msgs-fkie'
)

depends=('python2-docutils'
'python2-paramiko'
'ros-kinetic-default-cfg-fkie'
'ros-kinetic-diagnostic-msgs'
'ros-kinetic-dynamic-reconfigure'
'ros-kinetic-master-discovery-fkie'
'ros-kinetic-master-sync-fkie'
'ros-kinetic-multimaster-msgs-fkie'
'ros-kinetic-python-qt-binding'
'ros-kinetic-rosgraph'
'ros-kinetic-roslaunch'
'ros-kinetic-roslib'
'ros-kinetic-rosmsg'
'ros-kinetic-rospy'
'ros-kinetic-rosservice'
'ros-kinetic-rqt-gui'
'ros-kinetic-rqt-reconfigure'
'screen'
'xterm'
)

conflicts=()
replaces=()

_dir=node_manager_fkie
source=()
md5sums=()

prepare() {
    cp -R $startdir/node_manager_fkie $srcdir/node_manager_fkie
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

