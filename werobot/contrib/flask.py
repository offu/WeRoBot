# -*- coding: utf-8 -*-
from __future__ import absolute_import
from werobot.parser import parse_xml, process_message
from werobot.replies import process_function_reply
import logging


def make_view(robot):
    """
    为一个 BaseRoBot 生成 Flask view。

    :param robot: 一个 BaseRoBot 实例
    :return: 一个标准的 Flask view
    """
    from flask import request, make_response

    def werobot_view():
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        signature = request.args.get('signature', '')
        if not robot.check_signature(
                timestamp,
                nonce,
                signature,
        ):
            return 'Invalid Request.', 403
        if request.method == 'GET':
            return request.args['echostr']

        body = request.data
        message_dict = parse_xml(body)
        # Encrypt support
        if "Encrypt" in message_dict:
            xml = robot.crypto.decrypt_message(
                timestamp=timestamp,
                nonce=nonce,
                msg_signature=signature,
                encrypt_msg=message_dict["Encrypt"]
            )
            message_dict = parse_xml(xml)

        message = process_message(message_dict)
        logging.info("Receive message %s" % message)
        reply = robot.get_reply(message)
        if not reply:
            return ''
        # Encrypt support
        if robot.use_encryption:
            response = make_response(
                robot.crypto.encrypt_message(reply))
        else:
            response = make_response(
                process_function_reply(reply, message=message).render())
        response.headers['content_type'] = 'application/xml'
        return response

    return werobot_view
