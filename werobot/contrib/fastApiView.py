#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
import asyncio
from fastapi import Request,Response
from fastapi.responses import HTMLResponse
import html

def make_view(robot):
    """
    为一个 BaseRoBot 生成 fastapi view。
    用法：
        app = FastAPI()
        app.add_route('/werobot', make_view(robot), ['post'])
    :param robot:
    :return:
    """
    def werobot_view(request: Request):
        timestamp = request.query_params.get('timestamp')
        nonce = request.query_params.get('nonce')
        signature = request.query_params.get('signature')
        if not robot.check_signature(
                timestamp,
                nonce,
                signature,
        ):
            return HTMLResponse(robot.make_error_page(html.escape(request.url.hostname)), 403)
        message = robot.parse_message(
            asyncio.run(request.body()),
            timestamp=timestamp,
            nonce=nonce,
            msg_signature=request.query_params.get('msg_signature', '')
        )
        response = Response(robot.get_encrypted_reply(message))
        response.headers['content_type'] = 'application/xml'
        return response

    return werobot_view
