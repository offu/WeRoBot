# -*- coding: utf-8 -*-
from __future__ import absolute_import
from tornado.web import RequestHandler, HTTPError
from werobot.contrib.error import get_error_content


def make_handler(robot):
    """
    为一个 BaseRoBot 生成 Tornado Handler。

    Usage ::

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

    :param robot: 一个 BaseRoBot 实例。
    :return: 一个标准的 Tornado Handler
    """

    class WeRoBotHandler(RequestHandler):
        def prepare(self):
            timestamp = self.get_argument('timestamp', '')
            nonce = self.get_argument('nonce', '')
            signature = self.get_argument('signature', '')

            if not robot.check_signature(
                    timestamp=timestamp,
                    nonce=nonce,
                    signature=signature
            ):
                raise HTTPError(403, 'Invalid Request.')

        def get(self):
            echostr = self.get_argument('echostr', '')
            self.write(echostr)

        def post(self):
            timestamp = self.get_argument('timestamp', '')
            nonce = self.get_argument('nonce', '')
            msg_signature = self.get_argument('msg_signature', '')
            message = robot.parse_message(
                self.request.body,
                timestamp=timestamp,
                nonce=nonce,
                msg_signature=msg_signature
            )
            self.set_header("Content-Type",
                            "application/xml;charset=utf-8")
            self.write(robot.get_encrypted_reply(message))

    return WeRoBotHandler


def make_error_handler():
    """
    生成一个 Tornado Handler 展示错误页面

    :return: 一个标准的 Tornado Handler
    """

    class ErrorHandler(RequestHandler):
        def get(self, *args, **kwargs):
            self.set_header("Content-Type",
                            "text/html")
            self.write(get_error_content())

    return ErrorHandler
