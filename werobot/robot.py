# -*- coding: utf-8 -*-

import inspect
import hashlib

from bottle import Bottle, request, response, abort

from .parser import parse_user_msg
from .reply import create_reply

__all__ = ['BaseRoBot', 'WeRoBot']


class BaseRoBot(object):
    def __init__(self, token=None):
        self._handlers = {
            "subscribe": [],
            "unsubscribe": [],
            "click": [],
            "link": [],
            "text": [],
            "image": [],
            "location": [],
            "unknown": []
        }
        self.token = token

    def handler(self, f):
        """
        Decorator to add a new handler to the robot.
        """
        self.add_handler(f, types=[])
        return f

    def text(self, f):
        """
        Decorator to add a new handler to the robot.
        """
        self.add_handler(f, types=['text'])
        return f

    def image(self, f):
        """
        Decorator to add a new handler to the robot.
        """
        self.add_handler(f, types=['image'])
        return f

    def location(self, f):
        """
        Decorator to add a new handler to the robot.
        """
        self.add_handler(f, types=['location'])
        return f

    def link(self, f):
        self.add_handler(f, types=['link'])
        return f

    def subscribe(self, f):
        self.add_handler(f, types=['subscribe'])

    def unsubscribe(self, f):
        self.add_handler(f, types=['unsubscribe'])

    def click(self, f):
        self.add_handler(f, types=['click'])

    def unknown(self, f):
        """
        Decorator to add a new handler to the robot.
        """
        self.add_handler(f, types=['unknown'])
        return f

    def add_handler(self, func, types=None):
        """
        Add a new handler to the robot.
        """
        if not types:
            types = self._handlers.keys()
        if not inspect.isfunction(func):
            raise TypeError
        for type in types:
            self._handlers[type].append(func)

    def _get_reply(self, message):
        for handler in self._handlers[message.type]:
            reply = handler(message)
            if reply:
                return reply

    def check_signature(self, timestamp, nonce, signature):
        sign = [self.token, timestamp, nonce]
        sign.sort()
        sign = ''.join(sign)
        sign = hashlib.sha1(sign).hexdigest()
        return sign == signature


class WeRoBot(BaseRoBot):

    @property
    def wsgi(self):
        if not self._handlers:
            raise
        app = Bottle()

        @app.get('/')
        def echo():
            if not self.check_signature(
                request.query.timestamp,
                request.query.nonce,
                request.query.signature
            ):
                return abort('403')
            return request.query.echostr

        @app.post('/')
        def handle():
            if not self.check_signature(
                request.query.timestamp,
                request.query.nonce,
                request.query.signature
            ):
                return abort('403')

            body = request.body.read()
            message = parse_user_msg(body)
            reply = self._get_reply(message)
            if not reply:
                return ''
            response.content_type = 'application/xml'
            return create_reply(reply, message=message)

        return app

    def run(self, server='auto', host='127.0.0.1', port=8888):
        self.wsgi.run(server=server, host=host, port=port)
