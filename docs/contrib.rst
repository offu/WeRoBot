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

如果有必要，你还可以调用 :func:`werobot.contrib.django.make_error_view`，加入一个 error page ::

    from django.conf.urls import patterns, include, url
    from werobot.contrib.django import make_view, make_error_view
    from robot import robot

    urlpatterns = patterns('',
        url(r'^robot/', make_view(robot)),
        url(r'^/', make_error_view())
    )

Flask
----------
首先, 同样在文件中写好你的微信机器人 ::

    # Filename: robot.py

    from werobot import WeRoBot

    robot = WeRoBot(token='token')


    @robot.handler
    def hello(message):
        return 'Hello World!'

然后, 在 Flask 项目中为 Flask 实例集成 WeRoBot ::

    from flask import Flask
    from robot import robot
    from werobot.contrib.flask import make_view

    app = Flask(__name__)
    app.add_url_rule(rule='/robot/', # WeRoBot 挂载地址
                     endpoint='werobot', # Flask 的 endpoint
                     view_func=make_view(robot),
                     methods=['GET', 'POST'])

如果有必要，你可以调用 :func:`werobot.contrib.flask.make_error_view`，加入一个 error page ::

    from flask import Flask
    from robot import robot
    from werobot.contrib.flask import make_view, make_error_view

    app = Flask(__name__)
    app.add_url_rule(rule='/robot/', # WeRoBot 挂载地址
                     endpoint='werobot', # Flask 的 endpoint
                     view_func=make_view(robot),
                     methods=['GET', 'POST'])
    app.add_url_rule(rule='/',
                     view_func=make_error_view,
                     methods=['GET', 'POST'])

Bottle
--------
在你的 Bottle App 中集成 WeRoBot ::

    from werobot import WeRoBot

    robot = WeRoBot(token='token')

    @robot.handler
    def hello(message):
        return 'Hello World!'

    from bottle import Bottle
    from werobot.contrib.bottle import make_view

    app = Bottle()
    app.route('/robot',  # WeRoBot 挂载地址
             ['GET', 'POST'],
             make_view(robot))

如果有必要，调用 :func:`werobot.contrib.bottle.make_error_view`，加入一个 error page ::

    from werobot import WeRoBot
    from werobot.contrib.bottle import make_error_view

    robot = WeRoBot(token='token')

    @robot.handler
    def hello(message):
        return 'Hello World!'

    from bottle import Bottle
    from werobot.contrib.bottle import make_view

    app = Bottle()
    app.route('/robot',  # WeRoBot 挂载地址
             ['GET', 'POST'],
             make_view(robot))
    app.route('/',
             ['GET', 'POST'],
             make_error_view())

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

如果有必要，调用 :func:`werobot.contrib.tornado.make_error_handler`，加入一个 error page ::

    import tornado.ioloop
    import tornado.web
    from werobot import WeRoBot
    from werobot.contrib.tornado import make_handler, make_error_handler

    robot = WeRoBot(token='token')


    @robot.handler
    def hello(message):
        return 'Hello World!'

    application = tornado.web.Application([
        (r"/robot", make_handler(robot)),
        (r"/", make_error_handler())
    ])

    if __name__ == "__main__":
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

API
----------

.. module:: werobot.contrib.django
.. autofunction:: make_view

.. module:: werobot.contrib.django
.. autofunction:: make_error_view

.. module:: werobot.contrib.flask
.. autofunction:: make_view

.. module:: werobot.contrib.flask
.. autofunction:: make_error_view

.. module:: werobot.contrib.bottle
.. autofunction:: make_view

.. module:: werobot.contrib.bottle
.. autofunction:: make_error_view

.. module:: werobot.contrib.tornado
.. autofunction:: make_handler

.. module:: werobot.contrib.tornado
.. autofunction:: make_error_handler
