#!/usr/bin/env bash
set -x
brew update

case $PYTHON_INSTALL_METHOD in
    tox)
      brew install pyenv
      brew outdated pyenv || brew upgrade pyenv
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

pip install --upgrade pip wheel

brew install redis
brew services start redis
brew install mongodb
brew services start mongodb

brew install openssl
python --version
env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" pip install -r dev-requirements.txt
