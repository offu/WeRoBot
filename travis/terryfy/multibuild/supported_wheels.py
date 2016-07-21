#!/usr/bin/env python
"""  Filter out wheel filenames not supported on this platform
"""
from __future__ import print_function

import sys

from wheel.install import WheelFile
from pip.pep425tags import get_supported


def main():
    supported = set(get_supported())
    for fname in sys.argv[1:]:
        tags = set(WheelFile(fname).tags)
        if supported.intersection(tags):
            print(fname)


if __name__ == '__main__':
    main()
