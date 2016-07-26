#!/usr/bin/env bash

if [ $PYTHON_INSTALL_METHOD == "tox" ]; then
  tox
else
  coverage run --source werobot -m py.test
fi