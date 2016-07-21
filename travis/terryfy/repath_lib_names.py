""" Change install names and ids to reflect changed path
"""

USAGE = """\
USAGE: repath_lib_names.py <old_path> <new_path> <lib_fname> [<lib_fname, ...]
"""

from os.path import islink, isfile
import sys

from delocate.tools import (get_install_names, set_install_name,
                            get_install_id, set_install_id)


def repath_lib(lib_fname, old_path, new_path):
    install_id = get_install_id(lib_fname)
    L = len(old_path)
    if install_id and install_id.startswith(old_path):
        set_install_id(lib_fname, new_path + install_id[L:])
    for name in get_install_names(lib_fname):
        if name.startswith(old_path):
            set_install_name(lib_fname, name, new_path + name[L:])


def main():
    if len(sys.argv) < 4:
        print(USAGE)
        sys.exit(-1)
    old_path, new_path = sys.argv[1:3]
    for lib_fname in sys.argv[3:]:
        if isfile(lib_fname) and not islink(lib_fname):
            repath_lib(lib_fname, old_path, new_path)


if __name__ == '__main__':
    main()
