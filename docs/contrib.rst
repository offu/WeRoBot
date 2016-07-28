与其他 Web 框架集成
===================

WeRoBot 可以作为独立服务运行，也可以集成在其他 Web 框架中一同运行。

Django
--------
WeRoBot 支持 Django 1.7+。

首先，在一个文件中写好你的微信机器人 ::

    # Filename: robot.py

    from werobot import WeRoBot

    robot = WeRoBot(token='token')


    @robot.handler
    def hello(message):
        return 'Hello World!'

然后，在你 Django 项目中的 ``urls.py`` 中调用 :func:`werobot.contrib.django.make_view` ，将 WeRoBot 集成进 Django ::

    from django.conf.urls import patterns, include, url
    from werobot.contrib.django import make_view
    from robot import robot

    urlpatterns = patterns('',
        url(r'^robot/', make_view(robot)),
    )


大功告成。

API
----

.. module:: werobot.contrib.django
.. autofunction:: make_view
