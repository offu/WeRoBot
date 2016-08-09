# -*- coding: utf-8 -*-
from __future__ import absolute_import

from bottle import request, abort


def make_view(robot):
    """
    为一个 BaseRoBot 生成 Flask view。

    Usage ::
        from werobot import WeRoBot

        robot = WeRoBot(token='token')


        @robot.handler
        def hello(message):
            return 'Hello World!'

        from bottle import Bottle
        from werobot.contrib.bottle import make_view

        app = Bottle()
        app.route(
            '/robot',  # WeRoBot 挂载地址
            ['GET', 'POST'],
            make_view(robot)
        )


    :param robot: 一个 BaseRoBot 实例
    :return: 一个标准的 Flask view
    """
    def werobot_view(*args, **kwargs):
        if not robot.check_signature(
            request.query.timestamp,
            request.query.nonce,
            request.query.signature
        ):
            return abort(403)
        if request.method == 'GET':
            return request.query.echostr
        else:
            body = request.body.read()
            message = robot.parse_message(
                body,
                timestamp=request.query.timestamp,
                nonce=request.query.nonce,
                msg_signature=request.query.msg_signature
            )
            return robot.get_encrypted_reply(message)
    return werobot_view
