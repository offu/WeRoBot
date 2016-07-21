# Test multibuild utilities
source common_utils.sh
source tests/utils.sh

source tests/test_common_utils.sh
if [ -n "$IS_OSX" ]; then
    source osx_utils.sh
    get_macpython_environment $PYTHON_VERSION $VENV
    source tests/test_python_install.sh
    source tests/test_fill_pyver.sh
    source tests/test_osx_utils.sh
else
    source manylinux_utils.sh
    source tests/test_manylinux_utils.sh
fi

# Exit 1 if any test errors
barf
