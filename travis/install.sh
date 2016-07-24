#!/usr/bin/env bash
brew update

case $PYTHON_INSTALL_METHOD in
    tox)
      brew install pyenv
      eval "$(pyenv init -)"
      for version in $PYTHON_VERSION
      do
          pyenv install $version -s
      done
      pyenv local $PYTHON_VERSION
      ;;
    *)
      source travis/terryfy/library_installers.sh
      clean_builds
      get_python_environment $PYTHON_INSTALL_METHOD $PYTHON_VERSION venv
      ;;
esac

brew install redis
brew services start redis
brew install mongodb
brew services start mongodb
pip install --upgrade pip wheel
pip install -r dev-requirements.txt
python --version
