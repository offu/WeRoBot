# Some debug echoes
echo "Python on path: `which python`"
echo "Python cmd: $PYTHON_EXE"
echo "pip on path: $(which pip)"
echo "pip cmd: $PIP_CMD"
echo "virtualenv on path: $(which virtualenv)"
echo "virtualenv cmd: $VIRTUALENV_CMD"

# Check that a pip install puts scripts on path
pip install delocate
delocate-listdeps --version || ingest "Delocate not installed right"

# Python version from Python to compare against required
python_version=$($PYTHON_EXE --version 2>&1 | awk '{print $2}')
python_mm="${PYTHON_VERSION:0:1}.${PYTHON_VERSION:2:1}"

if [ "$python_version" != $PYTHON_VERSION ]; then
    ingest "Wrong macpython python version $python_version"
fi

if [ -n "$VENV" ]; then  # in virtualenv
    # Correct pip and Python versions should be on PATH
    if [ "$($PYTHON_EXE --version)" != "$(python --version)" ]; then
        ingest "Python versions do not match"
    fi
    if [ "$($PIP_CMD --version)" != "$(pip --version)" ]; then
        ingest "Pip versions do not match"
    fi
    # Versions in environment variables have full path
    if [ "$PYTHON_EXE" != "$PWD/venv/bin/python" ]; then
        ingest "Wrong virtualenv python '$PYTHON_EXE'"
    fi
    if [ "$PIP_CMD" != "$PWD/venv/bin/pip" ]; then
        ingest "Wrong virtualenv pip '$PIP_CMD'"
    fi
else # not virtualenv
    macpie_bin="$MACPYTHON_PY_PREFIX/$python_mm/bin"
    if [ "$PYTHON_EXE" != "$macpie_bin/python$python_mm" ]; then
        ingest "Wrong macpython python cmd '$PYTHON_EXE'"
    fi
    if [ "$PIP_CMD" != "sudo $macpie_bin/pip$python_mm" ]; then
        ingest "Wrong macpython pip '$PIP_CMD'"
    fi
fi
