#!/usr/bin/env bash
brew update

MAJOR_MAC_VERSION=$(sw_vers -productVersion | awk -F '.' '{print $1 "." $2}')
if [ $MAJOR_MAC_VERSION == "10.11" ]; then
  # https://github.com/rvm/rvm/pull/3627
  rvm get head
fi

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
pip install -r dev-requirements.txt

brew install redis
brew services start redis
if [ $MAJOR_MAC_VERSION == "10.9" ]; then
    curl -O https://fastdl.mongodb.org/osx/mongodb-osx-x86_64-3.2.10.tgz
    tar -zxvf mongodb-osx-x86_64-3.2.10.tgz
    sudo mkdir -p /data/db
    sudo ./mongodb-osx-x86_64-3.2.10/bin/mongod &
else
    brew install mongodb
    brew services start mongodb
fi
brew install openssl
python --version
