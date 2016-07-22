# Some debug echoes
echo "Python on path: `which python`"
echo "Python cmd: $PYTHON_EXE"
$PYTHON_EXE --version
if [ $? -ne 0 ] ; then RET=1; fi

echo "pip on path: `which pip`"
echo "pip cmd: $PIP_CMD"
$PIP_CMD --version
if [ $? -ne 0 ] ; then RET=1; fi

echo "virtualenv on path: `which virtualenv`"
echo "virtualenv cmd: $VIRTUALENV_CMD"

# Check that a pip install puts scripts on path
$PIP_CMD install delocate
delocate-listdeps --version
if [ $? -ne 0 ] ; then RET=1; fi

# Run the site-packages command
echo "Site packages: `get_py_site_packages`"
if [ $? -ne 0 ] ; then RET=1; fi

# Python version information
python_version=`$PYTHON_EXE -c \
    'import sys; print("{}.{}.{}".format(*sys.version_info[:3]))'`
python_mm=${python_version:0:3}
python_m=${python_version:0:1}

case $INSTALL_TYPE in
macpython)
    if [ "$python_version" != $(fill_pyver $VERSION) ]; then
        echo "Wrong macpython python version"
        RET=1
    fi
    ;;
system|macports)
    if [ "$python_mm" != "$VERSION" ]; then
        echo "Wrong macports python version"
        RET=1
    fi
    ;;
homebrew)
    if [ "$python_m" != "$VERSION" ]; then
        echo "Wrong homebrew python version"
        RET=1
    fi
    ;;
esac
if [ -n "$VENV" ]; then
    if [ "$PYTHON_EXE" != "$PWD/venv/bin/python" ]; then
        echo "Wrong virtualenv python"
        RET = 1
    fi
    if [ "$PIP_CMD" != "$PWD/venv/bin/pip" ]; then
        echo "Wrong virtualenv pip"
        RET=1
    fi
    # Check site-packages toggling doesn't error (at least)
    toggle_py_sys_site_packages
    toggle_py_sys_site_packages
    if [ $? -ne 0 ] ; then RET=1; fi
else # not virtualenv
    case $INSTALL_TYPE in
    system)
        if [ "$PYTHON_EXE" != "/usr/bin/python" ]; then
            echo "Wrong system python cmd"
            RET=1
        fi
        if [ "$PIP_CMD" != "sudo /usr/local/bin/pip" ]; then
            echo "Wrong system pip"
            RET=1
        fi
        ;;
    macpython)
        macpie_bin="$MACPYTHON_PY_PREFIX/$python_mm/bin"
        if [ "$PYTHON_EXE" != "$macpie_bin/python$python_mm" ]; then
            echo "Wrong macpython python cmd"
            RET=1
        fi
        if [ "$PIP_CMD" != "sudo $macpie_bin/pip$python_mm" ]; then
            echo "Wrong macpython pip"
            RET=1
        fi
        ;;
    macports)
        macports_pie_bin="$MACPORTS_PY_PREFIX/$python_mm/bin"
        if [ "$PYTHON_EXE" != "$macports_pie_bin/python$python_mm" ]; then
            echo "Wrong macports python cmd"
            RET=1
        fi
        if [ "$PIP_CMD" != "sudo /opt/local/bin/pip-$python_mm" ]; then
            echo "Wrong macports pip"
            RET=1
        fi
        ;;
    homebrew)
        if [ "$PYTHON_EXE" != "/usr/local/bin/python$python_m" ]; then
            echo "Wrong homebrew python cmd"
            RET=1
        fi
        if [ "$PIP_CMD" != "/usr/local/bin/pip$python_m" ]; then
            echo "Wrong homebrew pip"
            RET=1
        fi
        ;;
    esac
fi

# Check sudo
if [ -n "$VENV" ] || [ "$INSTALL_TYPE" == "homebrew" ]; then
    # Sudo should be empty
    if [ -n "`get_pip_sudo`" ]; then
        echo "pip sudo should be empty"
        RET=1
    fi
else # sudo should be set
    if [ "`get_pip_sudo`" != "sudo" ]; then
        echo "pip sudo not set"
        RET=1
    fi
fi
