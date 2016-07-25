#!/usr/bin/env bash

if [ $PYTHON_VERSION == "tox" ]; then
  tox
else
  coverage run --source werobot -m py.test
fi