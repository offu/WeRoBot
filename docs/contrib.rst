与其他 Web 框架集成
===================

WeRoBot 可以作为独立服务运行，也可以集成在其他 Web 框架中一同运行。

Django
--------
WeRoBot 支持 Django 1.8+。

首先，在一个文件中写好你的微信机器人 ::

    # Filename: robot.py

    from werobot import WeRoBot

    myrobot = WeRoBot(token='token')


    @myrobot.handler
    def hello(message):
        return 'Hello World!'

然后，在你 Django 项目中的 ``urls.py`` 中调用 :func:`werobot.contrib.django.make_view` ，将 WeRoBot 集成进 Django ::

    from django.conf.urls import patterns, include, url
    from werobot.contrib.django import make_view
    from robot import myrobot

    urlpatterns = patterns('',
        url(r'^robot/', make_view(myrobot)),
    )

.. module:: werobot.contrib.django
.. autofunction:: make_view

Flask
----------
首先, 同样在文件中写好你的微信机器人 ::

    # Filename: robot.py

    from werobot import WeRoBot

    myrobot = WeRoBot(token='token')


    @myrobot.handler
    def hello(message):
        return 'Hello World!'

然后, 在 Flask 项目中为 Flask 实例集成 WeRoBot ::

    from flask import Flask
    from robot import myrobot
    from werobot.contrib.flask import make_view

    app = Flask(__name__)
    app.add_url_rule(rule='/robot/', # WeRoBot 挂载地址
                     endpoint='werobot', # Flask 的 endpoint
                     view_func=make_view(myrobot),
                     methods=['GET', 'POST'])

.. module:: werobot.contrib.flask
.. autofunction:: make_view


Bottle
--------
在你的 Bottle App 中集成 WeRoBot ::

    from werobot import WeRoBot

    myrobot = WeRoBot(token='token')

    @myrobot.handler
    def hello(message):
        return 'Hello World!'

    from bottle import Bottle
    from werobot.contrib.bottle import make_view

    app = Bottle()
    app.route('/robot',  # WeRoBot 挂载地址
             ['GET', 'POST'],
             make_view(myrobot))

.. module:: werobot.contrib.bottle
.. autofunction:: make_view

Tornado
----------
最简单的 Hello World ::

    import tornado.ioloop
    import tornado.web
    from werobot import WeRoBot
    from werobot.contrib.tornado import make_handler

    myrobot = WeRoBot(token='token')


    @myrobot.handler
    def hello(message):
        return 'Hello World!'

    application = tornado.web.Application([
        (r"/robot/", make_handler(myrobot)),
    ])

    if __name__ == "__main__":
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

.. module:: werobot.contrib.tornado
.. autofunction:: make_handler
