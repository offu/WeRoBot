与其他 Web 框架集成
===================

WeRoBot 可以作为独立服务运行，也可以集成在其他 Web 框架中一同运行。

Django
--------
WeRoBot 支持 Django 1.6+。

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

Flask
----------
给你的 Flask 应用添加 WeRoBot 支持。
你可以在实例化 FlaskWeRoBot 的时候传入一个 Flask App 添加支持： ::

    from flask import Flask
    from werobot.contrib.flask import FlaskWeRoBot

    app = Flask(__name__)
    robot = FlaskWeRoBot(app)

或者也可以先实例化一个 FlaskWeRoBot ，然后通过 ``init_app`` 来给应用添加支持 ::

    from flask import Flask
    from werobot.contrib.flask import FlaskWeRoBot

    robot = FlaskWeRoBot()
    def create_app():
        app = Flask(__name__)
        robot.init_app(app)
        return app

Tornado
----------
最简单的 Hello World ::

    import tornado.ioloop
    import tornado.web
    from werobot import WeRoBot
    from tornado_werobot import make_handler

    robot = WeRoBot(token='token')


    @robot.handler
    def hello(message):
        return 'Hello World!'

    application = tornado.web.Application([
        (r"/", make_handler(robot)),
    ])

    if __name__ == "__main__":
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

API
----------

.. module:: werobot.contrib.django
.. autofunction:: make_view

.. module:: werobot.contrib.flask
.. autoclass:: FlaskWeRoBot
    :members: init_app

.. module:: werobot.contrib.tornado
.. autofunction:: make_handler
