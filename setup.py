#!/usr/bin/env python
# coding=utf-8

import io
import werobot

from setuptools import setup, find_packages

with io.open("README.rst", encoding="utf8") as f:
    readme = f.read().replace("develop", "master")
readme = readme.replace("latest", werobot.__version__)

setup(
    name='WeRoBot',
    version=werobot.__version__,
    author=werobot.__author__,
    author_email='whtsky@me.com',
    url='https://github.com/whtsky/WeRoBot',
    packages=find_packages(),
    keywords="wechat weixin werobot",
    description='WeRoBot: writing WeChat Offical Account Robots with fun',
    long_description=readme,
    setup_requires=[
        'pytest-runner',
    ],
    install_requires=open("requirements.txt").readlines(),
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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    tests_require=['pytest'],
)
