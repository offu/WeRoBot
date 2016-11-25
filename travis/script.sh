#!/usr/bin/env bash

if [ $PYTHON_INSTALL_METHOD == "tox" ] && [ $TEST_NUMBER == "1" ]; then
  env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" tox -e $(tox -l | grep -v py3 | tr "\n" ",")
elif [ $PYTHON_INSTALL_METHOD == "tox" ] && [ $TEST_NUMBER == "2" ]; then
  env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" tox -e $(tox -l | grep py3 | tr "\n" ",")
else
  python setup.py install
  coverage run --source werobot -m py.test
fi