#!/bin/bash
# Wheel build, install, run test steps on Linux
#
# In fact the main work is to wrap up the real functions in docker commands.
# The real work is in the BUILD_SCRIPT (which builds the wheel) and
# `docker_install_run.sh`, which can be configured with `config.sh`.
#
# Must define
#  before_install
#  build_wheel
#  install_run
set -e

MANYLINUX_URL=${MANYLINUX_URL:-https://nipy.bic.berkeley.edu/manylinux}

# Get our own location on this filesystem
MULTIBUILD_DIR=$(dirname "${BASH_SOURCE[0]}")

# Allow travis Python version as proxy for multibuild Python version
MB_PYTHON_VERSION=${MB_PYTHON_VERSION:-$TRAVIS_PYTHON_VERSION}

function before_install {
    # Install a virtualenv to work in.
    virtualenv --python=python venv
    source venv/bin/activate
    python --version # just to check
    pip install --upgrade pip wheel
}

function build_wheel {
    # Builds wheel, puts into $WHEEL_SDIR
    #
    # In fact wraps the actual work which happens in the container.
    #
    # Depends on
    #     REPO_DIR  (or via input argument)
    #     PLAT (can be passed in as argument)
    #     MB_PYTHON_VERSION
    #     BUILD_COMMIT
    #     UNICODE_WIDTH (optional)
    #     BUILD_DEPENDS (optional)
    #     MANYLINUX_URL (optional)
    #     WHEEL_SDIR (optional)
    local repo_dir=${1:-$REPO_DIR}
    [ -z "$repo_dir" ] && echo "repo_dir not defined" && exit 1
    local plat=${2:-$PLAT}
    local docker_image=quay.io/pypa/manylinux1_$plat
    docker pull $docker_image
    docker run --rm \
        -e PYTHON_VERSION="$MB_PYTHON_VERSION" \
        -e UNICODE_WIDTH="$UNICODE_WIDTH" \
        -e BUILD_COMMIT="$BUILD_COMMIT" \
        -e WHEEL_SDIR="$WHEEL_SDIR" \
        -e MANYLINUX_URL="$MANYLINUX_URL" \
        -e BUILD_DEPENDS="$BUILD_DEPENDS" \
        -e REPO_DIR="$repo_dir" \
        -e PLAT="$PLAT" \
        -v $PWD:/io \
        $docker_image /io/$MULTIBUILD_DIR/docker_build_wrap.sh
}

function install_run {
    # Install wheel, run tests
    #
    # In fact wraps the actual work which happens in the container.
    #
    # Depends on
    #  PLAT (can be passed in as argument)
    #  MB_PYTHON_VERSION
    #  UNICODE_WIDTH (optional)
    #  WHEEL_SDIR (optional)
    #  MANYLINUX_URL (optional)
    #  TEST_DEPENDS  (optional)
    local plat=${1:-$PLAT}
    bitness=$([ "$plat" == i686 ] && echo 32 || echo 64)
    local docker_image="matthewbrett/trusty:$bitness"
    docker pull $docker_image
    docker run --rm \
        -e PYTHON_VERSION="$MB_PYTHON_VERSION" \
        -e UNICODE_WIDTH="$UNICODE_WIDTH" \
        -e WHEEL_SDIR="$WHEEL_SDIR" \
        -e MANYLINUX_URL="$MANYLINUX_URL" \
        -e TEST_DEPENDS="$TEST_DEPENDS" \
        -v $PWD:/io \
        $docker_image /io/$MULTIBUILD_DIR/docker_test_wrap.sh
}
