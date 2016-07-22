#!/bin/bash
# Use with ``source travis_tools.sh``

# Get our own location on this filesystem
TERRYFY_DIR=$(dirname "${BASH_SOURCE[0]}")

# Get multibuild utilities
(cd $TERRYFY_DIR && git submodule update --init)
source $TERRYFY_DIR/multibuild/osx_utils.sh

MACPORTS_URL=https://distfiles.macports.org/MacPorts
MACPORTS_PKG=MacPorts-2.3.3-10.9-Mavericks.pkg
MACPORTS_PREFIX=/opt/local
MACPORTS_PY_PREFIX=$MACPORTS_PREFIX$MACPYTHON_PY_PREFIX
# -q to avoid this:
# https://lists.macosforge.org/pipermail/macports-users/2014-June/035672.html
PORT_INSTALL="sudo port -q install"
NIPY_WHEELHOUSE=https://nipy.bic.berkeley.edu/scipy_installers


function require_success {
    local status=$?
    local message=$1
    if [ "$status" != "0" ]; then
        echo $message
        exit $status
    fi
}


function get_py_site_packages {
    # Return site-packages directory using PYTHON_EXE
    check_python
    $PYTHON_EXE -c "from distutils import sysconfig; print(sysconfig.get_python_lib())"
}


function toggle_py_sys_site_packages {
    # When in virtualenv (not checked) toggle use of system site packages
    local no_sp_fname="`get_py_site_packages`/../no-global-site-packages.txt"
    if [ -f "$no_sp_fname" ]; then
        rm $no_sp_fname
    else
        touch $no_sp_fname
    fi
}

function pyver_ge {
    # Echo 1 if first python version is greater or equal to second
    # Parameters
    #   $first (python version in major.minor.extra format)
    #   $second (python version in major.minor.extra format)
    if [ $(lex_ver $1) -ge $(lex_ver $2) ]; then echo 1; fi
}


function get_pip_sudo {
    # Echo "sudo" if PIP_CMD starts with sudo
    # Useful for checking if Python installations need sudo
    check_pip
    if [ "${PIP_CMD:0:4}" == "sudo" ]; then
        echo "sudo"
    fi
}


function install_macports {
    # Initialize macports, put macports on PATH
    local macports_path=$DOWNLOADS_SDIR/$MACPORTS_PKG
    mkdir -p $DOWNLOADS_SDIR
    curl $MACPORTS_URL/$MACPORTS_PKG > $macports_path
    require_success "failed to download macports"
    sudo installer -pkg $macports_path -target /
    require_success "failed to install macports"
    PATH=$MACPORTS_PREFIX/bin:$PATH
    sudo port -v selfupdate
}


function macports_install_python {
    # Installs macports python
    # Parameter $version
    # Version given in format major.minor e.g. "3.4"
    # sets $PYTHON_EXE variable to python executable
    local py_version=$1
    local force=$2
    if [ "$force" == "1" ]; then
        force="-f"
    fi
    local py_mm=${py_version:0:3}
    local py_mm_nodot=`echo $py_mm | tr -d '.'`
    $PORT_INSTALL $force python$py_mm_nodot
    require_success "Failed to install macports python"
    PYTHON_EXE=`realpath $MACPORTS_PREFIX/bin/python$py_mm`
}


function macports_install_pip {
    # macports install of pip
    # Gets needed version from version implied by $PYTHON_EXE
    local py_mm=`get_py_mm`
    local py_mm_nodot=`get_py_mm_nodot`
    $PORT_INSTALL py$py_mm_nodot-pip
    PIP_CMD="sudo $MACPORTS_PREFIX/bin/pip-$py_mm"
}


function macports_install_virtualenv {
    # macports install of virtualenv
    # Gets needed version from version implied by $PYTHON_EXE
    local py_mm=`get_py_mm`
    local py_mm_nodot=`get_py_mm_nodot`
    $PORT_INSTALL py$py_mm_nodot-virtualenv
    VIRTUALENV_CMD="$MACPORTS_PREFIX/bin/virtualenv-$py_mm"
}


function brew_install_python {
    # Installs homebrew python
    # Parameter $version
    # Version can only be "2" or "3"
    # sets $PYTHON_EXE variable to python executable
    local py_version=$1
    local py_digit=${py_version:0:1}
    if [[ "$py_digit" == "3" ]] ; then
        brew install python3
    else
        brew install python
        # Now easy_install and pip are in /usr/local we need to force link
        brew link --overwrite python
    fi
    require_success "Failed to install python"
    PYTHON_EXE=/usr/local/bin/python$py_digit
}


function brew_set_pip_cmd {
    # homebrew set of $PIP_CMD variable
    # pip already installed by Python formula
    # Gets version from version implied by $PYTHON_EXE
    # https://github.com/Homebrew/homebrew/wiki/Homebrew-and-Python
    local py_digit=`get_py_digit`
    PIP_CMD=/usr/local/bin/pip${py_digit}
}


function patch_sys_python {
    # Fixes error discussed here:
    # http://stackoverflow.com/questions/22313407/clang-error-unknown-argument-mno-fused-madd-python-package-installation-fa
    # Present for OSX 10.9.2 fixed in 10.9.3
    # This should be benign for 10.9.3 though
    local py_sys_dir="/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7"
    pushd $py_sys_dir
    if [ -n "`grep fused-madd _sysconfigdata.py`" ]; then
        sudo sed -i '.old' 's/ -m\(no-\)\{0,1\}fused-madd//g' _sysconfigdata.py
        sudo rm _sysconfigdata.pyo _sysconfigdata.pyc
    fi
    popd
}


function system_install_pip {
    # Install pip into system python
    sudo easy_install pip
    PIP_CMD="sudo /usr/local/bin/pip"
}


function system_install_virtualenv {
    # Install virtualenv into system python
    # Needs $PIP_CMD
    check_pip
    $PIP_CMD install virtualenv
    require_success "Failed to install virtualenv"
    VIRTUALENV_CMD="/usr/local/bin/virtualenv"
}


function rename_wheels {
    local wheelhouse=$1
    check_var $wheelhouse
    # From https://github.com/minrk/wheelhouse/blob/master/wheelhouse.sh
    # tell pip that all of the 10.6 intel wheels will also work on 10.10
    # (System Python) and for x86_64
    for file in $(find "$wheelhouse" -name '*-macosx_10_6_intel.whl'); do
        mv $file $(echo $file | sed s/macosx_10_6_intel.whl/macosx_10_6_intel.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl/)
    done
}


function get_python_environment {
    # Set up python environment
    # Parameters:
    #     $install_type : {macpython|macports|homebrew|system}
    #         Type of Python to install
    #     $version :
    #         macpython : major.minor.micro e.g. "3.4.1"
    #         macpports : major.minor e.g. "3.4"
    #         homebrew : major e.g "3"
    #         system : ignored (but required to be not empty)
    #     $venv_dir : {directory_name|not defined}
    #         If defined - make virtualenv in this directory, set python / pip
    #         commands accordingly
    #
    # Installs Python
    # Sets $PYTHON_EXE to path to Python executable
    # Sets $PIP_CMD to full command for pip (including sudo if necessary)
    # If $venv_dir defined, Sets $VIRTUALENV_CMD to virtualenv executable
    # Puts directory of $PYTHON_EXE on $PATH
    local install_type=$1
    local version=$2
    local venv_dir=$3
    # Install python, pip, maybe virtualenv for different systems
    case $install_type in
    macpython)
        get_macpython_environment $version $venv_dir
        return
        ;;
    macports)
        remove_travis_ve_pip
        install_macports
        macports_install_python $version
        macports_install_pip
        if [ -n "$venv_dir" ]; then
            macports_install_virtualenv
            make_workon_venv $venv_dir
        fi
        ;;
    homebrew)
        # Homebrew already installed on travis worker
        remove_travis_ve_pip
        brew update
        brew_install_python $version
        brew_set_pip_cmd
        if [ -n "$venv_dir" ]; then
            install_virtualenv
            make_workon_venv $venv_dir
        fi
        ;;
    system)
        PYTHON_EXE="/usr/bin/python"
        remove_travis_ve_pip
        system_install_pip
        if [ -n "$venv_dir" ]; then
            system_install_virtualenv
            make_workon_venv $venv_dir
        fi
        ;;
    *)
        echo "Strange install type $install_type"
        exit 1
        ;;
    esac
    set_py_vars
}


TRAVIS_TOOLS_DIR=`realpath $( dirname "$BASH_SOURCE[0]}" )`

function checkout_closest_tag {
    # Check out tag closest to origin/master
    # Parameters
    #   submodule  (name of submodule)
    #   branch (name of branch to start from; optional, default "master")
    local submodule=$1
    check_var $submodule
    local branch=$2
    if [ -z "$branch" ]; then branch=master; fi
    cd $submodule
    git fetch
    git fetch --tags
    git checkout `$TRAVIS_TOOLS_DIR/git-closest-tag origin/$branch`
    cd ..
}


function checkout_commit {
    # Check out named commit or latest
    # Parameters
    #   submodule  (name of submodule)
    #   commitish ('latest-tag' or a git ref; optional, default
    #       'master')
    #   branch (name of branch to start 'latest-tag' from; optional,
    #       default "master")
    local submodule=$1
    check_var $submodule
    local commitish=$2
    if [ -z "$commitish" ]; then commitish=master; fi
    local branch=$3
    if [ -z "$branch" ]; then branch=master; fi
    cd $submodule
    git fetch
    git fetch --tags
    if [ "$commitish" == 'latest-tag' ]; then
        commitish=`$TRAVIS_TOOLS_DIR/git-closest-tag $branch`
    fi
    git checkout $commitish
    cd ..
}
