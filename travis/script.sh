#!/usr/bin/env bash

if [ $PYTHON_INSTALL_METHOD == "tox" ] && [ "$PYTHON_VERSION" == "pypy-5.0.0 2.7.12" ]; then
  env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" tox -e $(tox -l | grep -v py3 | tr "\n" ",")
elif [ $PYTHON_INSTALL_METHOD == "tox" ] && [ "$PYTHON_VERSION" == "3.5.2 3.4.5" ]; then
  env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" tox -e $(tox -l | grep py3 | tr "\n" ",")
else
  python setup.py install
  coverage run --source werobot -m py.test
fi