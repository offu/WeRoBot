#!/usr/bin/env bash
brew services list
if [ $PYTHON_INSTALL_METHOD == "tox" ]; then
  env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" tox -e $(tox -l | grep $PYTHON_MAJOR | tr "\n" ",")
else
  python setup.py install
  coverage run --source werobot -m py.test
fi