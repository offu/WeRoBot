#!/usr/bin/env bash

brew install pyenv
brew outdated pyenv || brew upgrade pyenv
brew install libffi
brew install ncurses
brew install zlib
eval "$(pyenv init -)"
for version in $PYTHON_VERSION
  do
    pyenv install $version -s
  done
pyenv local $PYTHON_VERSION

pip install --upgrade pip wheel

brew install openssl
python --version
env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include -I$(xcrun --show-sdk-path)/usr/include" pip install -r dev-requirements.txt
