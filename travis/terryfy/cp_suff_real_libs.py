""" Copy real (not symlinks to) libraries with given suffix
"""

from __future__ import print_function

USAGE = """\
cp_suff_real_libs.py <lib_dir> <lib_suffix>
"""

import os
from os.path import splitext, join as pjoin, islink
import sys
import shutil

LIB_EXTS = ('.a', '.so', '.dylib')


def main():
    try:
        lib_dir, suffix = sys.argv[1:]
    except (IndexError, ValueError):
        print(USAGE)
        sys.exit(-1)
    for fname in os.listdir(lib_dir):
        if not splitext(fname)[1] in LIB_EXTS:
            continue
        old_path = pjoin(lib_dir, fname)
        if islink(old_path):
            continue
        shutil.copyfile(old_path, old_path + suffix)


if __name__ == '__main__':
    main()
