""" Monkey patch waf code to pipe command output direct to stdout

As far as I know there is no way to do this using standard waf build commands
options.
"""

import sys
from waflib import Utils, Errors, Logs, Context


def my_exec_command(self,cmd,**kw):
    """ Copy of Context.exec_command that doesn't capture stdout / stderr

    This is necessary to prevent travis-ci timing out while waiting for
    feedback from the scipy build process, in particular
    """
    subprocess=Utils.subprocess
    kw['shell']=isinstance(cmd,str)
    Logs.debug('runner: %r'%cmd)
    Logs.debug('runner_env: kw=%s'%kw)
    if self.logger:
        self.logger.info(cmd)
    if'stdout'not in kw:
        kw['stdout']=sys.stdout
    if'stderr'not in kw:
        kw['stderr']=sys.stderr
    try:
        if kw['stdout']or kw['stderr']:
            p=subprocess.Popen(cmd,**kw)
            (out,err)=p.communicate()
            ret=p.returncode
        else:
            out,err=(None,None)
            ret=subprocess.Popen(cmd,**kw).wait()
    except Exception as e:
        raise Errors.WafError('Execution failure: %s'%str(e),ex=e)
    if out:
        if not isinstance(out,str):
            out=out.decode(sys.stdout.encoding or'iso8859-1')
        if self.logger:
            self.logger.debug('out: %s'%out)
        else:
            sys.stdout.write(out)
    if err:
        if not isinstance(err,str):
            err=err.decode(sys.stdout.encoding or'iso8859-1')
        if self.logger:
            self.logger.error('err: %s'%err)
        else:
            sys.stderr.write(err)
    return ret


def monkey_patch():
    """ Apply monkey patch to exec_command """
    Context.Context.exec_command = my_exec_command
