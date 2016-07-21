#!/bin/bash
# Utilities for both OSX and Docker Linux
# Python should be on the PATH
set -e

MULTIBUILD_DIR=$(dirname "${BASH_SOURCE[0]}")
if [ $(uname) == "Darwin" ]; then IS_OSX=1; fi

function abspath {
    python -c "import os.path; print(os.path.abspath('$1'))"
}

function relpath {
    # Path of first input relative to second (or $PWD if not specified)
    python -c "import os.path; print(os.path.relpath('$1','${2:-$PWD}'))"
}

function realpath {
    python -c "import os; print(os.path.realpath('$1'))"
}

function lex_ver {
    # Echoes dot-separated version string padded with zeros
    # Thus:
    # 3.2.1 -> 003002001
    # 3     -> 003000000
    echo $1 | awk -F "." '{printf "%03d%03d%03d", $1, $2, $3}'
}

function unlex_ver {
    # Reverses lex_ver to produce major.minor.micro
    # Thus:
    # 003002001 -> 3.2.1
    # 003000000 -> 3.0.0
    echo "$((10#${1:0:3}+0)).$((10#${1:3:3}+0)).$((10#${1:6:3}+0))"
}

function strip_ver_suffix {
    echo $(unlex_ver $(lex_ver $1))
}

function is_function {
    # Echo "true" if input argument string is a function
    # Allow errors during "set -e" blocks.
    (set +e; echo $($(declare -Ff "$1") > /dev/null && echo true))
}

function gh-clone {
    git clone https://github.com/$1
}

function rm_mkdir {
    # Remove directory if present, then make directory
    local path=$1
    if [ -z "$path" ]; then echo "Need not-empty path"; exit 1; fi
    if [ -d "$path" ]; then rm -rf $path; fi
    mkdir $path
}

function untar {
    local in_fname=$1
    if [ -z "$in_fname" ];then echo "in_fname not defined"; exit 1; fi
    local extension=${in_fname##*.}
    case $extension in
        tar) tar xf $in_fname ;;
        gz|tgz) tar zxf $in_fname ;;
        bz2) tar jxf $in_fname ;;
        zip) unzip $in_fname ;;
        xz) unxz -c $in_fname | tar xf ;;
        *) echo Did not recognize extension $extension; exit 1 ;;
    esac
}

function fetch_unpack {
    # Fetch input archive name from input URL
    # Parameters
    #    url - URL from which to fetch archive
    #    archive_fname (optional) archive name
    #
    # If `archive_fname` not specified then use basename from `url`
    # If `archive_fname` already present at download location, use that instead.
    local url=$1
    if [ -z "$url" ];then echo "url not defined"; exit 1; fi
    local archive_fname=${2:-$(basename $url)}
    local arch_sdir="${ARCHIVE_SDIR:-archives}"
    # Make the archive directory in case it doesn't exist
    mkdir -p $arch_sdir
    local out_archive="${arch_sdir}/${archive_fname}"
    # Fetch the archive if it does not exist
    if [ ! -f "$out_archive" ]; then
        curl -L $url > $out_archive
    fi
    # Unpack archive, refreshing contents
    rm_mkdir arch_tmp
    (cd arch_tmp && untar ../$out_archive && rsync --delete -avh * ..)
}

function clean_code {
    local repo_dir=${1:-$REPO_DIR}
    local build_commit=${2:-$BUILD_COMMIT}
    [ -z "$repo_dir" ] && echo "repo_dir not defined" && exit 1
    [ -z "$build_commit" ] && echo "build_commit not defined" && exit 1
    (cd $repo_dir \
        && git fetch origin \
        && git checkout $build_commit \
        && git clean -fxd \
        && git reset --hard \
        && git submodule update --init --recursive)
}

function build_wheel_cmd {
    # Builds wheel with named command, puts into $WHEEL_SDIR
    #
    # Parameters:
    #     cmd  (optional, default "pip_wheel_cmd"
    #        Name of command for builing wheel
    #     repo_dir  (optional, default $REPO_DIR)
    #
    # Depends on
    #     REPO_DIR  (or via input argument)
    #     WHEEL_SDIR  (optional, default "wheelhouse")
    #     BUILD_DEPENDS (optional, default "")
    #     MANYLINUX_URL (optional, default "") (via pip_opts function)
    local cmd=${1:-pip_wheel_cmd}
    local repo_dir=${2:-$REPO_DIR}
    [ -z "$repo_dir" ] && echo "repo_dir not defined" && exit 1
    local wheelhouse=$(abspath ${WHEEL_SDIR:-wheelhouse})
    if [ -n "$(is_function "pre_build")" ]; then pre_build; fi
    if [ -n "$BUILD_DEPENDS" ]; then
        pip install $(pip_opts) $BUILD_DEPENDS
    fi
    (cd $repo_dir && $cmd $wheelhouse)
    repair_wheelhouse $wheelhouse
}

function pip_wheel_cmd {
    local abs_wheelhouse=$1
    pip wheel $(pip_opts) -w $abs_wheelhouse --no-deps .
}

function bdist_wheel_cmd {
    # Builds wheel with bdist_wheel, puts into wheelhouse
    #
    # It may sometimes be useful to use bdist_wheel for the wheel building
    # process.  For example, versioneer has problems with versions which are
    # fixed with bdist_wheel:
    # https://github.com/warner/python-versioneer/issues/121
    local abs_wheelhouse=$1
    python setup.py bdist_wheel
    cp dist/*.whl $abs_wheelhouse
}

function build_pip_wheel {
    # Standard wheel building command with pip wheel
    build_wheel_cmd "pip_wheel_cmd" $@
}

function build_bdist_wheel {
    # Wheel building with bdist_wheel. See bdist_wheel_cmd
    build_wheel_cmd "bdist_wheel_cmd" $@
}

function build_wheel {
    # Set default building method to pip
    build_pip_wheel $@
}

function pip_opts {
    [ -n "$MANYLINUX_URL" ] && echo "--find-links $MANYLINUX_URL"
}

function get_platform {
    # Report platform as given by uname
    python -c 'import platform; print(platform.uname()[4])'
}

function install_wheel {
    # Install test dependencies and built wheel
    #
    # Pass any input flags to pip install steps
    #
    # Depends on:
    #     WHEEL_SDIR  (optional, default "wheelhouse")
    #     TEST_DEPENDS  (optional, default "")
    #     MANYLINUX_URL (optional, default "") (via pip_opts function)
    local wheelhouse=$(abspath ${WHEEL_SDIR:-wheelhouse})
    if [ -n "$TEST_DEPENDS" ]; then
        pip install $(pip_opts) $@ $TEST_DEPENDS
    fi
    # Install compatible wheel
    pip install $(pip_opts) $@ \
        $(python $MULTIBUILD_DIR/supported_wheels.py $wheelhouse/*.whl)
}

function install_run {
    # Depends on function `run_tests` defined in `config.sh`
    install_wheel
    mkdir tmp_for_test
    (cd tmp_for_test && run_tests)
}
