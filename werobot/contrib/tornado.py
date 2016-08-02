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
            message_dict = parse_xml(body)
            # Encrypt support
            if "Encrypt" in message_dict:
                xml = self.crypto.decrypt_message(
                    timestamp=timestamp,
                    nonce=nonce,
                    msg_signature=signature,
                    encrypt_msg=message_dict["Encrypt"]
                )
                message_dict = parse_xml(xml)

            message = process_message(message_dict)
            logging.info("Receive message %s" % message)
            self.set_header("Content-Type",
                            "application/xml;charset=utf-8")

            reply = robot.get_reply(message)
            if reply is None:
                self.write("")
                return
            # Encrypt support
            if robot.use_encryption:
                reply = robot.crypto.encrypt_message(reply)
            else:
                reply = process_function_reply(reply,
                                               message=message
                                               ).render()
            self.write(reply)

    return WeRoBotHandler
