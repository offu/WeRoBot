#!/usr/bin/env python
#coding=utf-8

import werobot

from setuptools import setup, find_packages

setup(
    name='WeRoBot',
    version=werobot.__version__,
    author=werobot.__author__,
    author_email='whtsky@me.com',
    url='https://github.com/whtsky/WeRoBot',
    packages=find_packages(),
    keywords="wechat weixin werobot",
    description='WeRoBot: writing WeChat Offical Account Robots with fun',
    long_description=open("README.rst").read().replace("latest", werobot.__version__),
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
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
)
