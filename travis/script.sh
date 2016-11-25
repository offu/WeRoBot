#!/usr/bin/env bash

if [ $PYTHON_INSTALL_METHOD == "tox" ]; then
  if [ $TEST_NUMBER == "1" ]; then
    env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" tox -c travis/tox-travis-1.ini
  else
    env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" tox -c travis/tox-travis-2.ini
  fi
else
  python setup.py install
  coverage run --source werobot -m py.test
fi