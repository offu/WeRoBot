#!/usr/bin/env bash
tox -e $(tox -l | grep -E $PYTHON_MAJOR | tr "\n" ",")
