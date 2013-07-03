import inspect
import hashlib

from bottle import Bottle, request, response, abort

from .parser import parse_user_msg
from .reply import create_reply
from .utils import py3k

__all__ = ['BaseRoBot', 'WeRoBot']


class BaseRoBot(object):
    message_types = ['subscribe', 'unsubscribe', 'click',  # event
                     'text', 'image', 'link', 'location']

    def __init__(self, token=None):
        self._handlers = dict((k, []) for k in self.message_types)
        self._handlers['fallback'] = lambda x, err: None
        self.token = token

    def handler(self, f):
        """
        Decorator to add a handler function for every messages
        """
        self.add_handler(f, types=[])
        return f

    def text(self, f):
        """
        Decorator to add a handler function for ``text`` messages
        """
        self.add_handler(f, types=['text'])
        return f

    def image(self, f):
        """
        Decorator to add a handler function for ``image`` messages
        """
        self.add_handler(f, types=['image'])
        return f

    def location(self, f):
        """
        Decorator to add a handler function for ``location`` messages
        """
        self.add_handler(f, types=['location'])
        return f

    def link(self, f):
        """
        Decorator to add a handler function for ``link`` messages
        """
        self.add_handler(f, types=['link'])
        return f

    def subscribe(self, f):
        """
        Decorator to add a handler function for ``subscribe event`` messages
        """
        self.add_handler(f, types=['subscribe'])

    def unsubscribe(self, f):
        """
        Decorator to add a handler function for ``unsubscribe event`` messages
        """
        self.add_handler(f, types=['unsubscribe'])

    def click(self, f):
        """
        Decorator to add a handler function for ``click`` messages
        """
        self.add_handler(f, types=['click'])

    def fallback(self, f):
        """
        Decorator to register handler function for messages that have no relevant handlers
        """
        self.add_handler(f, types=['fallback'])

    def get_fallback_handler(self):
        return self._handlers['fallback']

    def add_handler(self, func, types=None):
        """
        Add a handler function for messages of given types.
        """
        if not types:
            types = self._handlers.keys()
        if not inspect.isfunction(func):
            raise TypeError
        if types == 'fallback':
            self._handlers['fallback'] = func
        else:
            for type in types:
                self._handlers[type].append(func)

    def get_reply(self, message):
        """
        Return the raw xml reply for the given message.
        """
        try:
            for handler in self._handlers[message.type]:
                reply = handler(message)
                if reply:
                    return reply
        except Exception, e:
            fallback = self.get_fallback_handler()
            fallback(message, e)

    def check_signature(self, timestamp, nonce, signature):
        sign = [self.token, timestamp, nonce]
        sign.sort()
        sign = ''.join(sign)
        if py3k:
            sign = sign.encode()
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
            reply = self.get_reply(message)
            if not reply:
                return ''
            response.content_type = 'application/xml'
            return create_reply(reply, message=message)

        return app

    def run(self, server='auto', host='127.0.0.1', port=8888):
        self.wsgi.run(server=server, host=host, port=port)
