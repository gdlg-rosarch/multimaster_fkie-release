# Script generated with Bloom
pkgdesc="ROS - The metapackage to combine the nodes required to establish and manage a multimaster network. This requires no or minimal configuration. The changes are automatically detected and synchronized."
url='http://ros.org/wiki/multimaster_fkie'

pkgname='ros-kinetic-multimaster-fkie'
pkgver='0.7.8_1'
pkgrel=1
arch=('any')
license=('BSD'
)

makedepends=('ros-kinetic-catkin'
)

depends=('ros-kinetic-default-cfg-fkie'
'ros-kinetic-master-discovery-fkie'
'ros-kinetic-master-sync-fkie'
'ros-kinetic-multimaster-msgs-fkie'
'ros-kinetic-node-manager-fkie'
)

conflicts=()
replaces=()

_dir=multimaster_fkie
source=()
md5sums=()

prepare() {
    cp -R $startdir/multimaster_fkie $srcdir/multimaster_fkie
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

