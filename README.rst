====================================
WeRoBot
====================================

.. image:: https://travis-ci.org/whtsky/WeRoBot.svg?branch=develop
    :target: https://travis-ci.org/whtsky/WeRoBot
.. image:: https://ci.appveyor.com/api/projects/status/gc69rrbmm3qxhnq6/branch/develop?svg=true
    :target: https://ci.appveyor.com/project/whtsky/WeRoBot
.. image:: https://coveralls.io/repos/github/whtsky/WeRoBot/badge.svg?branch=develop 
    :target: https://coveralls.io/github/whtsky/WeRoBot?branch=develop
.. image:: https://scrutinizer-ci.com/g/whtsky/WeRoBot/badges/quality-score.png?b=develop
    :target: https://scrutinizer-ci.com/g/whtsky/WeRoBot/?branch=develop


WeRoBot 是一个微信机器人框架，采用MIT协议发布。

文档在这里： https://werobot.readthedocs.org/en/latest/

安装
========

推荐使用 pip 进行安装 ::

    pip install werobot

如果你没有安装 pip 而且正在使用一台 OS X / Linux 电脑，那么你应该运行 ::

    curl http://peak.telecommunity.com/dist/ez_setup.py | python
    curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python

如果你是 Windows 用户， 那么下载 http://peak.telecommunity.com/dist/ez_setup.py 和 https://raw.github.com/pypa/pip/master/contrib/get-pip.py 这两个文件，双击运行。

Hello World
=============

一个非常简单的 Hello World 微信机器人，会对收到的所有文本消息回复 Hello World ::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    @robot.text
    def hello_world():
        return 'Hello World!'

    robot.run()

Session
===========

WeRoBot 在 0.4.0 版本中开始支持 Session ， Session 可以用来方便的记录用户数据 ::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere', enable_session=True)

    @robot.text
    def session(message, session):
        last = session.get("last", None)
        if last:
            return last
        session["last"] = message.content
        return '这是你第一次和我说话'

    robot.run()

