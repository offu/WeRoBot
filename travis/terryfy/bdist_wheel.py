#!/usr/bin/env python
""" Script to run bdist_wheel after setuptools import
"""

import sys, os

import setuptools

def main():
    del sys.argv[0]
    if not sys.argv:
        sys.argv[:0] = ['setup.py']
    elif sys.argv[0].startswith('-'):
        sys.argv[:0] = ['setup.py']
    sys.argv.insert(1, 'bdist_wheel')
    if os.path.isdir(sys.argv[0]):
        sys.argv[0] = os.path.join(sys.argv[0], 'setup.py')
    path, name = os.path.split(os.path.abspath(sys.argv[0]))
    if path:
        os.chdir(path)
    sys.path.insert(0, path)
    sys.argv[0] = name
    g = dict(globals())
    g['__file__'] = sys.argv[0]
    g['__name__'] = '__main__'
    if sys.version_info[0] < 3:
        execfile(sys.argv[0], g, g)
    else:
        exec(open(sys.argv[0]).read(), g, g)


if __name__ == '__main__':
    main()
