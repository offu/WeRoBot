from __future__ import print_function

from os.path import split as psplit, join as pjoin
from subprocess import Popen, PIPE

def back_tick(cmd, ret_err=False, as_str=True, shell=False):
    """ Run command `cmd`, return stdout, or stdout, stderr if `ret_err`

    Roughly equivalent to ``check_output`` in Python 2.7

    Parameters
    ----------
    cmd : str
        command to execute
    ret_err : bool, optional
        If True, return stderr in addition to stdout.  If False, just return
        stdout
    as_str : bool, optional
        Whether to decode outputs to unicode string on exit.

    Returns
    -------
    out : str or tuple
        If `ret_err` is False, return stripped string containing stdout from
        `cmd`.  If `ret_err` is True, return tuple of (stdout, stderr) where
        ``stdout`` is the stripped stdout, and ``stderr`` is the stripped
        stderr.

    Raises
    ------
    Raises RuntimeError if command returns non-zero exit code
    """
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=shell)
    out, err = proc.communicate()
    retcode = proc.returncode
    if retcode is None:
        proc.terminate()
        raise RuntimeError(cmd + ' process did not terminate')
    if retcode != 0:
        raise RuntimeError(cmd + ' process returned code %d' % retcode)
    out = out.strip()
    if as_str:
        out = out.decode('latin-1')
    if not ret_err:
        return out
    err = err.strip()
    if as_str:
        err = err.decode('latin-1')
    return out, err


def seq_to_list(seq):
    """ Convert non-sequence to 1 element sequence, tuples to lists
    """
    if not isinstance(seq, (list, tuple)):
        return [seq]
    return list(seq)


class FilePackageMaker(object):
    # all packages
    instances = {}

    def __init__(self, name, filename, build_cmd,
                 depends=(),
                 after=(),
                 patcher=None,
                 unpacked_sdir=None,
                 build_src_sdir='src',
                ):
        """ Initialize object for creating unpack, patch, build tasks

        Unpacking assumed to have no dependencies.

        Patching assumed to depend only on the unpacking.

        Build depends on packing / patching and on given dependencies

        Parameters
        ----------
        name : str
            package name
        filename : str
            filename containing source archive to unpack
        build_cmd : str or callable
            command to build after extracting
        depends : str or sequence, optional
            depends for build
        after : str or sequence, optional
            names to set build to follow after (task name depends)
        patcher : None or str or callable, optional
            If str, a file containing a ``-p1`` patch for the sources.  If
            callable, then a rule to apply for patching. If None, don't patch
        unpacked_sdir : str or None, optional
            directory created by unpacking `filename`.  If None we guess from
            `filename`
        build_src_sdir : str, optional
            subdirectory in build directory into which to unpack
        """
        self.name = name
        self.filename = filename
        self.build_cmd = build_cmd
        _, fname = psplit(filename)
        if fname.endswith('.tar.gz'):
            self.unpack_cmd = 'tar zxf'
            fname = fname[:-7]
        elif fname.endswith('.tar.bz2'):
            self.unpack_cmd = 'tar jxf'
            fname = fname[:-8]
        elif fname.endswith('.zip'):
            self.unpack_cmd = 'unzip'
            fname = fname[:-4]
        else:
            raise ValueError("Can't work out type of archive " + fname)
        self.patcher = patcher
        if unpacked_sdir is None: # Guess at output subdirectory
            unpacked_sdir = fname
        self.unpacked_sdir = unpacked_sdir
        self.depends = seq_to_list(depends)
        self.after = seq_to_list(after)
        self.build_src_sdir = build_src_sdir
        self._register_instance()

    def _register_instance(self):
        """ Register instance to class dictionary """
        if self.name in self.instances:
            raise ValueError('Name "{0}" already in instance '
                             'dict'.format(self.name))
        self.instances[self.name] = self

    def _unpack(self, bctx):
        task_name = self.name + '.unpack'
        dir_relpath = pjoin(self.build_src_sdir, self.unpacked_sdir)
        dir_node = bctx.bldnode.make_node(dir_relpath)
        archive_path = pjoin(bctx.srcnode.abspath(), self.filename)
        rule  = 'cd {dir_path} && {unpack_cmd} {archive_path}'.format(
            dir_path = pjoin(bctx.bldnode.abspath(), self.build_src_sdir),
            unpack_cmd = self.unpack_cmd,
            archive_path = archive_path)
        bctx(rule = rule,
             target = dir_node,
             name = task_name)
        return task_name, dir_node

    def unpack_patch_build(self, bctx):
        """ Make task generators to unpack, patch and build

        Parameters
        ----------
        bctx : build context

        Returns
        -------
        build_name : str
            name of build task, for other tasks to depend on if necessary
        dir_node : :class:`Node` instance
            node pointing to directory containing unpacked and built sources
        """
        task_name, dir_node = self._unpack(bctx)
        if not self.patcher is None:
            if hasattr(self.patcher, '__call__'): # patch function
                rule = self.patcher
            else: # assume filename in source tree
                patch_node = bctx.srcnode.find_node(self.patcher)
                if patch_node is None:
                    bctx.fatal('Patch file {0} does not exist'.format(
                        self.patcher))
                rule = 'cd ${SRC} && patch -p1 < ' + patch_node.abspath()
            task_name = self.name + '.patch'
            bctx(
                rule = rule,
                source = dir_node,
                name = task_name)
        build_name = self.name + '.build'
        bctx(
            rule = self.build_cmd,
            source = [dir_node] + self.depends,
            after = [task_name] + self.after,
            name = build_name)
        return build_name, dir_node


class GitPackageMaker(FilePackageMaker):
    # all packages
    instances = {}

    def __init__(self, name, commit, build_cmd,
                 depends=(),
                 after=(),
                 patcher=None,
                 out_sdir=None,
                 git_sdir=None,
                 build_src_sdir='src',
                ):
        """ Initialize object for creating unpack, patch, build tasks

        * Unpacking assumed to have no dependencies.
        * Patching assumed to depend only on the unpacking.
        * Build depends on packing / patching and on given dependencies

        Parameters
        ----------
        name : str
            package name
        commit : str
            identifier for commit to unarchive
        build_cmd : str or callable
            command to build after extracting
        depends : str or sequence, optional
            depends for build
        after : str or sequence, optional
            names to set build to follow after (task name depends)
        patcher : None or str or callable, optional
            If str, a file containing a ``-p1`` patch for the sources.  If
            callable, then a rule to apply for patching. If None, don't patch
        out_sdir : None or str, optional
            subdirectory in `build_src_sdir` in which to unpack. If None, use
            `name`
        git_sdir : str or None, optional
            directory containing git repository.  Defaults to `name`
        build_src_sdir : str, optional
            subdirectory in build directory into which to unpack
        """
        self.name = name
        self.commit = commit
        self.build_cmd = build_cmd
        self.patcher = patcher
        if git_sdir is None:
            git_sdir = name
        self.git_sdir = git_sdir
        self.depends = seq_to_list(depends)
        self.after = seq_to_list(after)
        self.build_src_sdir = build_src_sdir
        self.out_sdir = name if out_sdir is None else out_sdir
        self._register_instance()

    def _unpack(self, bctx):
        src_path = bctx.srcnode.abspath()
        bld_path = bctx.bldnode.abspath()
        task_name = self.name + '.unpack'
        dir_relpath = pjoin(self.build_src_sdir, self.out_sdir)
        dir_node = bctx.bldnode.make_node(dir_relpath)
        git_dir = pjoin(src_path, self.git_sdir)
        bctx(
            rule = ('cd {git_dir} && '
                    'git archive --prefix={dir_relpath}/ {commit} | '
                    '( cd {bld_path} && tar x )'.format(
                        git_dir = git_dir,
                        dir_relpath = dir_relpath,
                        commit = self.commit,
                        bld_path = bld_path)),
            target = dir_node,
            name = task_name)
        return task_name, dir_node
