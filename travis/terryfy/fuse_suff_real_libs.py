""" Fuse real (not symlinks to) libraries with same name
"""

from __future__ import print_function

USAGE = """\
fuse_suff_real_libs.py <lib_dir_out> <lib_dir_in1> <lib_dir_in2>
"""

import os
from os.path import (splitext, join as pjoin, split as psplit, islink, isfile,
                     abspath, realpath)
import sys
import shutil
from subprocess import check_call

LIB_EXTS = ('.a', '.so', '.dylib')


def main():
    try:
        lib_dir_out, lib_dir_in1, lib_dir_in2 = sys.argv[1:]
    except (IndexError, ValueError):
        print(USAGE)
        sys.exit(-1)
    for fname in os.listdir(lib_dir_in1):
        if not splitext(fname)[1] in LIB_EXTS:
            continue
        lib_path = pjoin(lib_dir_in1, fname)
        out_path = pjoin(lib_dir_out, fname)
        if islink(lib_path):
            continue
        lib_path_2 = pjoin(lib_dir_in2, fname)
        if not isfile(lib_path_2):
            continue
        # Fuse and copy library
        check_call(['lipo', '-create', lib_path, lib_path_2,
                    '-output', out_path])


if __name__ == '__main__':
    main()
