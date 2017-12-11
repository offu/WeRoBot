#!/usr/bin/env bash
brew services list
env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" tox -e $(tox -l | grep -E $PYTHON_MAJOR | tr "\n" ",")
