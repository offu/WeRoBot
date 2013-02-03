import inspect
import logging

from bottle import Bottle, request, response, abort

from .parser import parse_user_msg
from .reply import create_reply
from .utils import enable_pretty_logging, check_token, check_signature

__all__ = ['WeRoBot']


class WeRoBot(object):
    def __init__(self, token):
        self._handlers = []
        if not check_token(token):
            raise AttributeError('%s is not a vaild token.' % token)
        self.token = token

    def handler(self, func):
        """
        Decorator to add a new handler to the robot.
        """
        self._handlers.append(func)
        return func

    def add_handler(self, func):
        """
        Add a new handler to the robot.
        """
        if not inspect.isfunction(func):
            raise TypeError
        self._handlers.append(func)

    @property
    def app(self):
        if not self._handlers:
            raise
        app = Bottle()

        @app.get('/')
        def echo():
            if not check_signature(self.token,
                request.query.timestamp,
                request.query.nonce,
                request.query.signature):
                return abort('403')
            return request.query.echostr

        @app.post('/')
        def handle():
            if not check_signature(self.token,
                request.query.timestamp,
                request.query.nonce,
                request.query.signature):
                return abort('403')

            body = request.body
            message = parse_user_msg(body).read()
            for handler in self._handlers:
                reply = handler(message)
                if reply:
                    response.content_type = 'application/xml;charset=utf-8'
                    return create_reply(reply, message=message)
            return '.'

        return app

    def run(self, port=8888):
        enable_pretty_logging()
        self.app.run(server='auto', host='0.0.0.0', port=port)
