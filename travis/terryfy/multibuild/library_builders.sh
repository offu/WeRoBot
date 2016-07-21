# Recipes for building some libaries
OPENBLAS_VERSION="${OPENBLAS_VERSION:-0.2.18}"
# We use system zlib by default - see build_new_zlib
ZLIB_VERSION="${ZLIB_VERSION:-1.2.8}"
LIBPNG_VERSION="${LIBPNG_VERSION:-1.6.21}"
BZIP2_VERSION="${BZIP2_VERSION:-1.0.6}"
FREETYPE_VERSION="${FREETYPE_VERSION:-2.6.3}"
TIFF_VERSION="${TIFF_VERSION:-4.0.6}"
OPENJPEG_VERSION="${OPENJPEG_VERSION:-2.1}"
LCMS2_VERSION="${LCMS2_VERSION:-2.7}"
GIFLIB_VERSION="${GIFLIB_VERSION:-5.1.3}"
LIBWEBP_VERSION="${LIBWEBP_VERSION:-0.5.0}"
XZ_VERSION="${XZ_VERSION:-5.2.2}"
LIBYAML_VERSION="${LIBYAML_VERSION:-0.1.5}"
SZIP_VERSION="${SZIP_VERSION:-2.1}"
HDF5_VERSION="${HDF5_VERSION:-1.8.17}"
LIBAEC_VERSION="${LIBAEC_VERSION:-0.3.3}"
BUILD_PREFIX="${BUILD_PREFIX:-/usr/local}"
ARCHIVE_SDIR=${ARCHIVE_DIR:-archives}

# Set default compilation flags and OSX flag variable
if [ $(uname) == "Darwin" ]; then
    # Dual arch build by default
    ARCH_FLAGS=${ARCH_FLAGS:-"-arch i386 -arch x86_64"}
    # Only set CFLAGS, FFLAGS if they are not already defined.  Build functions
    # can override the arch flags by setting CFLAGS, FFLAGS
    export CFLAGS="${CFLAGS:-$ARCH_FLAGS}"
    export FFLAGS="${FFLAGS:-$ARCH_FLAGS}"
    IS_OSX=1
fi

function build_simple {
    local name=$1
    local version=$2
    local url=$3
    if [ -e "${name}-stamp" ]; then
        return
    fi
    local name_version="${name}-${version}"
    local targz=${name_version}.tar.gz
    fetch_unpack $url/$targz
    (cd $name_version \
        && ./configure --prefix=$BUILD_PREFIX \
        && make \
        && make install)
    touch "${name}-stamp"
}

function build_openblas {
    if [ -e openblas-stamp ]; then return; fi
    if [ -d "OpenBLAS" ]; then
        (cd OpenBLAS && git clean -fxd && git reset --hard)
    else
        git clone https://github.com/xianyi/OpenBLAS
    fi
    (cd OpenBLAS \
        && git checkout "v${OPENBLAS_VERSION}" \
        && make DYNAMIC_ARCH=1 USE_OPENMP=0 NUM_THREADS=64 > /dev/null \
        && make PREFIX=$BUILD_PREFIX install)
    touch openblas-stamp
}

function build_zlib {
    # Gives an old but safe version
    if [ -e zlib-stamp ]; then return; fi
    # OSX has zlib already
    if [ -z "$IS_OSX" ]; then yum install -y zlib-devel; fi
    touch zlib-stamp
}

function build_new_zlib {
    # Careful, this one may cause yum to segfault
    build_simple zlib $ZLIB_VERSION http://zlib.net
}

function build_jpeg {
    if [ -e jpeg-stamp ]; then return; fi
    fetch_unpack http://ijg.org/files/jpegsrc.v9b.tar.gz
    (cd jpeg-9b \
        && ./configure --prefix=$BUILD_PREFIX \
        && make \
        && make install)
    touch jpeg-stamp
}

function build_libpng {
    build_zlib
    build_simple libpng $LIBPNG_VERSION http://download.sourceforge.net/libpng
}

function build_bzip2 {
    if [ -e bzip2-stamp ]; then return; fi
    fetch_unpack http://bzip.org/${BZIP2_VERSION}/bzip2-${BZIP2_VERSION}.tar.gz
    (cd bzip2-${BZIP2_VERSION} \
        && make -f Makefile-libbz2_so \
        && make install PREFIX=$BUILD_PREFIX)
    touch bzip2-stamp
}

function build_tiff {
    build_zlib
    build_jpeg
    build_openjpeg
    build_xz
    build_simple tiff $TIFF_VERSION http://download.osgeo.org/libtiff
}

function build_openjpeg {
    if [ -e openjpeg-stamp ]; then return; fi
    local cmake=cmake
    if [ -n "$IS_OSX" ]; then
        brew install cmake
    else
        yum install -y cmake28
        cmake=cmake28
    fi
    fetch_unpack https://github.com/uclouvain/openjpeg/archive/version.${OPENJPEG_VERSION}.tar.gz
    (cd openjpeg-version.${OPENJPEG_VERSION} \
        && $cmake -DCMAKE_INSTALL_PREFIX=$BUILD_PREFIX . \
        && make install)
    touch openjpeg-stamp
}

function build_lcms2 {
    build_tiff
    build_simple lcms2 $LCMS2_VERSION http://downloads.sourceforge.net/project/lcms/lcms/$LCMS2_VERSION
}

function build_giflib {
    build_simple giflib $GIFLIB_VERSION http://downloads.sourceforge.net/project/giflib
}

function build_xz {
    build_simple xz $XZ_VERSION http://tukaani.org/xz
}

function build_libwebp {
    if [ -e libwebp-stamp ]; then return; fi
    build_libpng
    build_tiff
    build_giflib
    fetch_unpack https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-${LIBWEBP_VERSION}.tar.gz
    (cd libwebp-${LIBWEBP_VERSION} && \
        ./configure --enable-libwebpmux --enable-libwebpdemux --prefix=$BUILD_PREFIX \
        && make \
        && make install)
    touch libwebp-stamp
}

function build_freetype {
    build_libpng
    build_bzip2
    build_simple freetype $FREETYPE_VERSION http://download.savannah.gnu.org/releases/freetype
}

function build_libyaml {
    build_simple yaml $LIBYAML_VERSION http://pyyaml.org/download/libyaml
}

function build_szip {
    # Build szip without encoding (patent restrictions)
    if [ -e szip-stamp ]; then return; fi
    build_zlib
    local szip_url=https://www.hdfgroup.org/ftp/lib-external/szip/
    fetch_unpack ${szip_url}/$SZIP_VERSION/src/szip-$SZIP_VERSION.tar.gz
    (cd szip-$SZIP_VERSION \
        && ./configure --enable-encoding=no --prefix=$BUILD_PREFIX \
        && make \
        && make install)
    touch szip-stamp
}

function build_hdf5 {
    if [ -e hdf5-stamp ]; then return; fi
    build_zlib
    # libaec is a drop-in replacement for szip
    build_libaec
    local hdf5_url=https://www.hdfgroup.org/ftp/HDF5/releases
    fetch_unpack $hdf5_url/hdf5-$HDF5_VERSION/src/hdf5-$HDF5_VERSION.tar.gz
    (cd hdf5-$HDF5_VERSION \
        && ./configure --with-szlib=$BUILD_PREFIX --prefix=$BUILD_PREFIX \
        && make \
        && make install)
    touch hdf5-stamp
}

function build_libaec {
    if [ -e libaec-stamp ]; then return; fi
    local root_name=libaec-0.3.3
    local tar_name=${root_name}.tar.gz
    # Note URL will change for each version
    fetch_unpack https://gitlab.dkrz.de/k202009/libaec/uploads/48398bd5b7bc05a3edb3325abfeac864/${tar_name}
    (cd $root_name \
        && ./configure --prefix=$BUILD_PREFIX \
        && make \
        && make install)
    touch libaec-stamp
}
