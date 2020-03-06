# -*- coding: utf-8 -*-

from tornado.web import RequestHandler

import html


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
                timestamp=timestamp, nonce=nonce, signature=signature
            ):
                self.set_status(403)
                self.write(
                    robot.make_error_page(
                        html.escape(
                            self.request.protocol + "://" + self.request.host +
                            self.request.uri
                        )
                    )
                )
                return

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
            self.set_header("Content-Type", "application/xml;charset=utf-8")
            self.write(robot.get_encrypted_reply(message))

    return WeRoBotHandler
