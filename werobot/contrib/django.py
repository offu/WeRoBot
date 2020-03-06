# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

import html


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
            timestamp=timestamp, nonce=nonce, signature=signature
        ):
            return HttpResponseForbidden(
                robot.make_error_page(
                    html.escape(request.build_absolute_uri())
                )
            )
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
