#!/bin/bash
# Wheel build, install, run test steps on OSX
set -e

# Get needed utilities
MULTIBUILD_DIR=$(dirname "${BASH_SOURCE[0]}")
MB_PYTHON_VERSION=${MB_PYTHON_VERSION:-$TRAVIS_PYTHON_VERSION}
source $MULTIBUILD_DIR/osx_utils.sh
source $MULTIBUILD_DIR/library_builders.sh

# NB - config.sh sourced at end of this function.
# config.sh can override any function defined here.

function before_install {
    export CC=clang
    export CXX=clang++
    get_macpython_environment $MB_PYTHON_VERSION venv
    source venv/bin/activate
    pip install --upgrade pip wheel
}

# build_wheel function defined in common_utils (via osx_utils)
# install_run function defined in common_utils

# Local configuration may define custom pre-build, source patching.
# It can also overwrite the functions above.
source config.sh
