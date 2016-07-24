#!/usr/bin/env bash
brew update

case $PYTHON_VERSION in
    system)
      curl https://bootstrap.pypa.io/get-pip.py | python
      pip install virtualenv
      virtualenv venv
      . venv/bin/active
      ;;
    tox)
      brew install pyenv
      eval "$(pyenv init -)"
      pyenv install 2.6.9
      pyenv install 2.7.12
      pyenv install 3.3.6
      pyenv install 3.4.5
      pyenv install 3.5.2
      pyenv install pypy-5.3.1
      pyenv local 2.6.9 2.7.12 3.3.6 3.4.5 3.5.2 pypy-5.3.1
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
