#!/usr/bin/env bash

if [ "$(uname)" == "Darwin" ]; then
  brew update
  brew install redis
  brew services start redis
  brew install mongodb
  brew services start mongodb

  source travis/terryfy/library_installers.sh
  clean_builds
  get_python_environment $PYTHON_INSTALL_METHOD $PYTHON_VERSION venv
fi

python setup.py install
pip install -r dev-requirements.txt