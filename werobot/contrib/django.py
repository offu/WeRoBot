# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import os
import io


def make_view(robot):
    """
    为一个 BaseRoBot 生成 Django view。

    :param robot: 一个 BaseRoBot 实例。
    :return: 一个标准的 Django view
    """

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
            with io.open(
                    os.path.join(os.path.dirname(__file__), 'error.html'), 'r', encoding='utf-8'
            ) as error_page:
                return HttpResponseForbidden(error_page.read())

        if request.method == "GET":
            return HttpResponse(request.GET.get("echostr", ""))
        elif request.method == "POST":
            message = robot.parse_message(
                request.body,
                timestamp=timestamp,
                nonce=nonce,
                msg_signature=request.GET.get("msg_signature", "")
            )
            return HttpResponse(
                robot.get_encrypted_reply(message),
                content_type="application/xml;charset=utf-8"
            )
        return HttpResponseNotAllowed(['GET', 'POST'])

    return werobot_view
