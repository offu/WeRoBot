""" Parse travis.yml file, partly
"""
import sys

if sys.version_info[0] > 2:
    basestring = str


class TravisError(Exception):
    pass


def get_yaml_entry(yaml_dict, name):
    """ Get entry `name` from dict `yaml_dict`

    Parameters
    ----------
    yaml_dict : dict
        dict or subdict from parsing .travis.yml file
    name : str
        key to analyze and return

    Returns
    -------
    entry : None or list
        If `name` not in `yaml_dict` return None.  If key value is a string
        return a single entry list. Otherwise return the key value.
    """
    entry = yaml_dict.get(name)
    if entry is None:
        return None
    if isinstance(entry, basestring):
        return [entry]
    return entry


def get_envs(yaml_dict):
    """ Get first env combination from travis yaml dict

    Parameters
    ----------
    yaml_dict : dict
        dict or subdict from parsing .travis.yml file

    Returns
    -------
    bash_str : str
        bash scripting lines as string
    """
    env = get_yaml_entry(yaml_dict, 'env')
    if env is None:
        return ''
    # Bare string
    if isinstance(env, basestring):
        return env + '\n'
    # Simple list defining matrix
    if isinstance(env, (list, tuple)):
        return env[0] + '\n'
    # More complex dictey things
    globals, matrix = [get_yaml_entry(env, name)
                       for name in ('global', 'matrix')]
    if hasattr(matrix, 'keys'):
        raise TravisError('Oops, envs too complicated')
    lines = []
    if not globals is None:
        if matrix is None:
            raise TravisError('global section needs matrix section')
        lines += globals
    if not matrix is None:
        lines.append(matrix[0])
    return '\n'.join(lines) + '\n'
