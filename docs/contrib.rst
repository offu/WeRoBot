Web 框架
============

WeRoBot 默认使用 Bottle 作为 web 框架, 你也可以使用 werobot.contrib 进行替换。

Django 支持
------------------------------
WeRoBot 支持 Django 1.7+。

首先，在一个文件中写好你的微信机器人 ::

    # Filename: robot.py

    from werobot import WeRoBot

    robot = WeRoBot(token='token')


    @robot.handler
    def hello(message):
        return 'Hello World!'

然后，在你 Django 项目中的 ``urls.py`` 中调用 :func:`make_view` ，将 WeRoBot 集成进 Django ::

    from django.conf.urls import patterns, include, url
    from werobot.contrib.werobot_django import make_view
    from robot import robot

    urlpatterns = patterns('',
        url(r'^robot/', make_view(robot)),
    )


大功告成。

API
------------------------------

.. module:: werobot.contrib.werobot_django
.. autofunction:: make_view

