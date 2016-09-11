# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from werobot.contrib.error import get_error_content


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
            return HttpResponseForbidden()

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


def make_error_view():
    """
    生成一个 Django view 展示错误页面

    :return: 一个标准的 Django view
    """

    @csrf_exempt
    def error_view():
        return HttpResponse(
            get_error_content(),
            content_type="text/html"
        )

    return error_view
