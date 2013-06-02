#!/usr/bin/env python
#coding=utf-8

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
    long_description="""
    WeRoBot 是一个简单好用的 Python 微信机器人框架。

    Hello World ::

        import werobot

        robot = werobot.WeRoBot(token='tokenhere')

        @robot.handler
        def echo(message):
            return 'Hello World!'

        robot.run()

    文档： https://werobot.readthedocs.org/en/v%s/index.html
    """ % werobot.__version__,
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
)
