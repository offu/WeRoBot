#!/usr/bin/env bash

if [ $PYTHON_INSTALL_METHOD == "tox" ] && [ $TEST_NUMBER == "1" ]; then
  env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" tox -c tox-travis-1.ini
elif [ $PYTHON_INSTALL_METHOD == "tox" ] && [ $TEST_NUMBER == "2" ]; then
  env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" tox -c tox-travis-2.ini
else
  python setup.py install
  coverage run --source werobot -m py.test
fi