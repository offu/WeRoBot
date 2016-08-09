# -*- coding: utf-8 -*-
from __future__ import absolute_import
from werobot.robot import BaseRoBot
from werobot.parser import parse_xml, process_message
from tornado.web import RequestHandler, HTTPError
from werobot.replies import process_function_reply
import logging


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
    assert isinstance(robot, BaseRoBot), \
        "RoBot should be an BaseRoBot instance."

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
            signature = self.get_argument('signature', '')
            body = self.request.body
            message = robot.parse_message(
                request.data,
                timestamp=timestamp,
                nonce=nonce,
                signature=signature
            )
            self.set_header("Content-Type",
                            "application/xml;charset=utf-8")
            self.write(self.get_encrypted_reply(message))

    return WeRoBotHandler
