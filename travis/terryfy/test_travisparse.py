""" Nosetests for travis2bashes script
"""
from __future__ import absolute_import, print_function

import os
import sys
sys.path.append(os.path.dirname(__file__))

from travisparse import get_envs, TravisError
from nose.tools import assert_equal, assert_true, assert_false, assert_raises


def test_get_envs():
    # Get fetch of environment from .travis.yml
    assert_equal(get_envs({}), '')
    assert_equal(get_envs(dict(install = ['something'])), '')
    yaml = dict(env = {'global': ['LATEST_TAG=1'],
                       'matrix': ['VERSION=2.7.8 NUMPY_VERSION=1.6.1',
                                  'VERSION=3.3.5 NUMPY_VERSION=1.7.1',
                                  'VERSION=3.4.1 NUMPY_VERSION=1.7.1']})
    assert_equal(get_envs(yaml),
"""LATEST_TAG=1
VERSION=2.7.8 NUMPY_VERSION=1.6.1
""")
    yaml = dict(env = {'matrix': ['VERSION=2.7.8 NUMPY_VERSION=1.6.1',
                                  'VERSION=3.3.5 NUMPY_VERSION=1.7.1',
                                  'VERSION=3.4.1 NUMPY_VERSION=1.7.1']})
    assert_equal(get_envs(yaml),
"""VERSION=2.7.8 NUMPY_VERSION=1.6.1
""")
    yaml = dict(env = ['ISOLATED=true', 'ISOLATED=false'])
    assert_equal(get_envs(yaml),
"""ISOLATED=true
""")
    # excludes too complicated
    yaml = dict(env = {'matrix':
                       {'exclude':
                        [{'gemfile': 'Gemfile', 'rvm': '2.0.0'}]}})
    assert_raises(TravisError, get_envs, yaml)
    # includes too complicated
    yaml = dict(env = {'matrix':
                       {'include':
                        [{'gemfile': 'gemfiles/Gemfile.rails-3.2.x',
                          'rvm': 'ruby-head',
                          'env': 'ISOLATED=false'}]}})
    assert_raises(TravisError, get_envs, yaml)
    # global implies matrix
    yaml = dict(env = {'global': ['LATEST_TAG=1']})
    assert_raises(TravisError, get_envs, yaml)
    # one line is OK too
    yaml = dict(env = {'global': 'LATEST_TAG=1',
                       'matrix': 'VERSION=3.3.1'})
    assert_equal(get_envs(yaml),
"""LATEST_TAG=1
VERSION=3.3.1
""")
    yaml = dict(env = 'MY_VAR=1')
    assert_equal(get_envs(yaml),
"""MY_VAR=1
""")
