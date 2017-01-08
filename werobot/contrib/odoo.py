# -*- coding: utf-8 -*-

__author__ = 'Jachin Lin'

from __future__ import absolute_import
from odoo.http import request


try:
    import html
except ImportError:
    import cgi as html


def make_view(robot):
    """
    为一个 BaseRoBot 生成 Odoo view。

    Usage ::

        from werobot import WeRoBot

        robot = WeRoBot(token='token')


        @robot.handler
        def hello(message):
            return 'Hello World!'

        from odoo import http
        from odoo.http import request

        class WeChat(http.Controller):

            @http.route('/wechat', type='http', auth="none", methods=['GET', 'POST'], csrf=False)
            def wechat(self, *args, **kwargs):
                return make_view(robot)()

                from flask import Flask
                from werobot.contrib.flask import make_view

    :param robot: 一个 BaseRoBot 实例
    :return: 一个标准的 Odoo view
    """

    def werobot_view():
        timestamp = request.params.get('timestamp', '')
        nonce = request.params.get('nonce', '')
        signature = request.params.get('signature', '')
        if not robot.check_signature(
                timestamp,
                nonce,
                signature,
        ):
            return robot.make_error_page(html.escape(request.httprequest.url)), 403
        if request.httprequest.method == 'GET':
            return request.params['echostr']

        message = robot.parse_message(
            request.httprequest.data,
            timestamp=timestamp,
            nonce=nonce,
            msg_signature=request.params.get('msg_signature', '')
        )
        response = request.make_response(robot.get_encrypted_reply(message))
        return response

    return werobot_view
