#!/bin/bash
# Install and test steps on Linux
set -e

# Get needed utilities
MULTIBUILD_DIR=$(dirname "${BASH_SOURCE[0]}")
source $MULTIBUILD_DIR/common_utils.sh

# Change into root directory of repo
cd /io

# Configuration for this package in `config.sh`.
# This can overwrite `install_run`' and `install_wheel` (called from
# `install_run`). These are otherwise defined in common_utils.sh.
# `config.sh` must define `run_tests` if using the default `install_run`.
source config.sh

install_run
