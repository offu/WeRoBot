# -*- coding: utf-8 -*-


from django.http import \
    HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from werobot.robot import BaseRoBot
from werobot.replies import process_function_reply
from werobot.parser import parse_xml, process_message
import logging


def make_view(robot):
    """
    为一个 BaseRoBot 生成 Django view。

    :param robot: 一个 BaseRoBot 实例。
    :return: 一个标准的 Django view
    """
    assert isinstance(robot, BaseRoBot), \
        "RoBot should be an BaseRoBot instance."

    @csrf_exempt
    def werobot_view(request):
        timestamp = request.GET.get("timestamp", "")
        nonce = request.GET.get("nonce", "")
        signature = request.GET.get("signature", "")

        if not robot.check_signature(
                timestamp=timestamp,
                nonce=nonce,
                signature=signature
        ):
            return HttpResponseForbidden()

        if request.method == "GET":
            return HttpResponse(request.GET.get("echostr", ""))
        elif request.method == "POST":
            body = request.body
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
                robot.logger.warning("No handler responded message %s"
                                     % message)
                return ''
            # Encrypt support
            if robot.use_encryption:
                return HttpResponse(
                    robot.crypto.encrypt_message(reply),
                    content_type="application/xml;charset=utf-8")
            return HttpResponse(
                process_function_reply(reply, message=message).render(),
                content_type="application/xml;charset=utf-8"
            )
        return HttpResponseNotAllowed(['GET', 'POST'])

    return werobot_view
