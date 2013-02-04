#!/usr/bin/env python
#coding=utf-8

import sys
kwargs = {}
major, minor = sys.version_info[:2]
if major >= 3:
    kwargs['use_2to3'] = True

from setuptools import setup, find_packages

import werobot

setup(
    name='WeRoBot',
    version=werobot.__version__,
    author='whtsky',
    author_email='whtsky@me.com',
    url='https://github.com/whtsky/WeRoBot',
    packages=find_packages(),
    description='WeRoBot: a robot framework for wechat',
    long_description=open('docs/index.rst').read(),
    install_requires=[
        'bottle'
    ],
    include_package_data=True,
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        ],
    tests_require=['nose'],
    test_suite='nose.collector',
    **kwargs
)
