#!/usr/bin/env bash
brew services list
env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" tox -e $(tox -l | grep $PYTHON_MAJOR | tr "\n" ",")
