#!/usr/bin/env bash
set -ex

if [ $PYTHON_VERSION == "tox" ]; then
  tox
else
  coverage run --source werobot -m py.test
fi