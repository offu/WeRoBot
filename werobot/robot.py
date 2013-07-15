import inspect
import hashlib
import logging

from bottle import Bottle, request, response, abort

from .parser import parse_user_msg
from .reply import create_reply
from .utils import py3k

__all__ = ['BaseRoBot', 'WeRoBot']


class BaseRoBot(object):
    message_types = ['subscribe', 'unsubscribe', 'click',  # event
                     'text', 'image', 'link', 'location']

    def __init__(self, token=None, logger=None, enable_session=False,
                 session_storage=None):
        self._handlers = dict((k, []) for k in self.message_types)
        self._handlers['all'] = []
        self.token = token
        if logger is None:
            logger = logging.getLogger("WeRoBot")
        self.logger = logger

        if enable_session and session_storage is None:
            from .session.filestorage import FileStorage
            session_storage = FileStorage()
        self.session_storage = session_storage

    def handler(self, f):
        """
        Decorator to add a handler function for every messages
        """
        self.add_handler(f, type='all')
        return f

    def text(self, f):
        """
        Decorator to add a handler function for ``text`` messages
        """
        self.add_handler(f, type='text')
        return f

    def image(self, f):
        """
        Decorator to add a handler function for ``image`` messages
        """
        self.add_handler(f, type='image')
        return f

    def location(self, f):
        """
        Decorator to add a handler function for ``location`` messages
        """
        self.add_handler(f, type='location')
        return f

    def link(self, f):
        """
        Decorator to add a handler function for ``link`` messages
        """
        self.add_handler(f, type='link')
        return f

    def subscribe(self, f):
        """
        Decorator to add a handler function for ``subscribe event`` messages
        """
        self.add_handler(f, type='subscribe')

    def unsubscribe(self, f):
        """
        Decorator to add a handler function for ``unsubscribe event`` messages
        """
        self.add_handler(f, type='unsubscribe')

    def click(self, f):
        """
        Decorator to add a handler function for ``click`` messages
        """
        self.add_handler(f, type='click')

    def add_handler(self, func, type='all'):
        """
        Add a handler function for messages of given type.
        """
        if not inspect.isfunction(func):
            raise TypeError
        self._handlers[type].append(func)

    def get_handlers(self, type):
        return self._handlers[type] + self._handlers['all']

    def get_reply(self, message):
        """
        Return the raw xml reply for the given message.
        """
        session_storage = self.session_storage
        if session_storage:
            id = message.source
            session = session_storage[id]
        handlers = self.get_handlers(message.type)
        try:
            for handler in handlers:
                if session_storage:
                    reply = handler(message, session)
                    session_storage[id] = session
                else:
                    reply = handler(message)
                if reply:
                    return reply
        except:
            self.logger.warning("Catch an exception", exc_info=True)

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
            logging.info("Receive message %s" % message)
            reply = self.get_reply(message)
            if not reply:
                self.logger.warning("No handler responded message %s"
                                    % message)
                return ''
            response.content_type = 'application/xml'
            return create_reply(reply, message=message)

        return app

    def run(self, server='auto', host='127.0.0.1',
            port=8888, enable_pretty_logging=True):
        if enable_pretty_logging:
            from werobot.utils import enable_pretty_logging
            enable_pretty_logging(self.logger)
        self.wsgi.run(server=server, host=host, port=port)
