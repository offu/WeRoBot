# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import six
import warnings

from werobot.config import Config, ConfigAttribute
from werobot.client import Client
from werobot.exceptions import ConfigError
from werobot.parser import parse_xml, process_message
from werobot.replies import process_function_reply
from werobot.utils import to_binary, to_text, check_signature, make_error_page, cached_property

try:
    from inspect import signature
except ImportError:
    from funcsigs import signature

__all__ = ['BaseRoBot', 'WeRoBot']

_DEFAULT_CONFIG = dict(
    TOKEN=None,
    SERVER="auto",
    HOST="127.0.0.1",
    PORT="8888",
    SESSION_STORAGE=None,
    APP_ID=None,
    APP_SECRET=None,
    ENCODING_AES_KEY=None
)


class BaseRoBot(object):
    message_types = ['subscribe_event', 'unsubscribe_event', 'click_event',
                     'view_event', 'scan_event',
                     'location_event', 'unknown_event',  # event
                     'text', 'image', 'link', 'location', 'voice', 'unknown']

    token = ConfigAttribute("TOKEN")
    session_storage = ConfigAttribute("SESSION_STORAGE")

    def __init__(self, token=None, logger=None,
                 enable_session=None, session_storage=None,
                 app_id=None, app_secret=None, encoding_aes_key=None,
                 config=None, **kwargs):
        self._handlers = dict((k, []) for k in self.message_types)
        self._handlers['all'] = []
        self.make_error_page = make_error_page

        if logger is None:
            import werobot.logger
            logger = werobot.logger.logger
        self.logger = logger

        if config is None:
            self.config = Config(_DEFAULT_CONFIG)
            self.config.update(
                TOKEN=token,
                APP_ID=app_id,
                APP_SECRET=app_secret,
                ENCODING_AES_KEY=encoding_aes_key
            )
            for k, v in kwargs.items():
                self.config[k.upper()] = v

            if enable_session is not None:
                warnings.warn(
                    "enable_session is deprecated."
                    "set SESSION_STORAGE to False if you want to disable Session",
                    DeprecationWarning,
                    stacklevel=2
                )
                if not enable_session:
                    self.config["SESSION_STORAGE"] = False

            if session_storage:
                self.config["SESSION_STORAGE"] = session_storage
        else:
            self.config = config

        self.use_encryption = False

    @cached_property
    def crypto(self):
        app_id = self.config.get("APP_ID", None)
        if not app_id:
            raise ConfigError(
                "You need to provide app_id to encrypt/decrypt messages"
            )

        encoding_aes_key = self.config.get("ENCODING_AES_KEY", None)
        if not encoding_aes_key:
            raise ConfigError(
                "You need to provide encoding_aes_key "
                "to encrypt/decrypt messages"
            )
        self.use_encryption = True

        from .crypto import MessageCrypt
        return MessageCrypt(
            token=self.config["TOKEN"],
            encoding_aes_key=encoding_aes_key,
            app_id=app_id
        )

    @cached_property
    def client(self):
        return Client(self.config)

    @cached_property
    def session_storage(self):
        if self.config["SESSION_STORAGE"] is False:
            return None
        if not self.config["SESSION_STORAGE"]:
            from .session.sqlitestorage import SQLiteStorage
            self.config["SESSION_STORAGE"] = SQLiteStorage()
        return self.config["SESSION_STORAGE"]

    @session_storage.setter
    def session_storage(self, value):
        warnings.warn(
            "You should set session storage in config",
            DeprecationWarning,
            stacklevel=2
        )
        self.config["SESSION_STORAGE"] = value

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

    def voice(self, f):
        """
        Decorator to add a handler function for ``voice`` messages
        """
        self.add_handler(f, type='voice')
        return f

    def unknown(self, f):
        """
        Decorator to add a handler function for ``unknown`` messages
        """
        self.add_handler(f, type='unknown')
        return f

    def subscribe(self, f):
        """
        Decorator to add a handler function for ``subscribe`` event
        """
        self.add_handler(f, type='subscribe_event')
        return f

    def unsubscribe(self, f):
        """
        Decorator to add a handler function for ``unsubscribe`` event
        """
        self.add_handler(f, type='unsubscribe_event')
        return f

    def click(self, f):
        """
        Decorator to add a handler function for ``click`` event
        """
        self.add_handler(f, type='click_event')
        return f

    def scan(self, f):
        """
        Decorator to add a handler function for ``scan`` event
        """
        self.add_handler(f, type='scan_event')
        return f

    def location_event(self, f):
        """
        Decorator to add a handler function for ``location`` event
        """
        self.add_handler(f, type='location_event')
        return f

    def view(self, f):
        """
        Decorator to add a handler function for ``view`` event
        """
        self.add_handler(f, type='view_event')
        return f

    def unknown_event(self, f):
        """
        Decorator to add a handler function for ``unknown`` event
        """
        self.add_handler(f, type='unknown_event')
        return f

    def key_click(self, key):
        """
        Shortcut for ``click`` messages
        @key_click('KEYNAME') for special key on click event
        """

        def wraps(f):
            argc = len(signature(f).parameters.keys())

            @self.click
            def onclick(message, session=None):
                if message.key == key:
                    return f(*[message, session][:argc])

            return f

        return wraps

    def filter(self, *args):
        """
        Shortcut for ``text`` messages
        ``@filter("xxx")``, ``@filter(re.compile("xxx"))``
        or ``@filter("xxx", "xxx2")`` to handle message with special content
        """

        content_is_list = False

        if len(args) > 1:
            content_is_list = True
        else:
            target_content = args[0]
            if isinstance(target_content, six.string_types):
                target_content = to_text(target_content)

                def _check_content(message):
                    return message.content == target_content
            elif hasattr(target_content, "match") \
                    and callable(target_content.match):
                # 正则表达式什么的

                def _check_content(message):
                    return target_content.match(message.content)
            else:
                raise TypeError(
                    "%s is not a valid target_content" % target_content
                )

        def wraps(f):
            if content_is_list:
                for x in args:
                    self.filter(x)(f)
                return f
            argc = len(signature(f).parameters.keys())

            @self.text
            def _f(message, session=None):
                if _check_content(message):
                    return f(*[message, session][:argc])

            return f

        return wraps

    def add_handler(self, func, type='all'):
        """
        Add a handler function for messages of given type.
        """
        if not callable(func):
            raise ValueError("{} is not callable".format(func))

        self._handlers[type].append((func, len(signature(func).parameters.keys())))

    def get_handlers(self, type):
        return self._handlers.get(type, []) + self._handlers['all']

    def parse_message(self, body, timestamp=None, nonce=None, msg_signature=None):
        """
        解析获取到的 Raw XML ，如果需要的话进行解密，返回 WeRoBot Message。
        :param body: 微信服务器发来的请求中的 Body。
        :return: WeRoBot Message
        """
        message_dict = parse_xml(body)
        if "Encrypt" in message_dict:
            xml = self.crypto.decrypt_message(
                timestamp=timestamp,
                nonce=nonce,
                msg_signature=msg_signature,
                encrypt_msg=message_dict["Encrypt"]
            )
            message_dict = parse_xml(xml)
        return process_message(message_dict)

    def get_reply(self, message):
        """
        Return the Reply Object for the given message.
        """
        session_storage = self.session_storage

        id = None
        session = None
        if session_storage and hasattr(message, "source"):
            id = to_binary(message.source)
            session = session_storage[id]

        handlers = self.get_handlers(message.type)
        try:
            for handler, args_count in handlers:
                args = [message, session][:args_count]
                reply = handler(*args)
                if session_storage and id:
                    session_storage[id] = session
                if reply:
                    return process_function_reply(reply, message=message)
        except:
            self.logger.warning("Catch an exception", exc_info=True)

    def get_encrypted_reply(self, message):
        """
        对一个指定的 WeRoBot Message ，获取 handlers 处理后得到的 Reply。
        如果可能，对该 Reply 进行加密。
        返回 Reply Render 后的文本。
        :param message: 一个 WeRoBot Message 实例。
        :return: reply （纯文本）
        """
        reply = self.get_reply(message)
        if not reply:
            self.logger.warning("No handler responded message %s"
                                % message)
            return ''
        if self.use_encryption:
            return self.crypto.encrypt_message(reply)
        else:
            return reply.render()

    def check_signature(self, timestamp, nonce, signature):
        return check_signature(
            self.config["TOKEN"], timestamp, nonce, signature
        )

    def error_page(self, f):
        """
        为 robot 指定 Signature 验证不通过时显示的错误页面。
        Usage ::
            @robot.error_page
            def make_error_page(url):
                return "<h1>喵喵喵 %s 不是给麻瓜访问的快走开</h1>" % url
        """
        self.make_error_page = f
        return f


class WeRoBot(BaseRoBot):
    @cached_property
    def wsgi(self):
        if not self._handlers:
            raise
        from bottle import Bottle
        from werobot.contrib.bottle import make_view

        app = Bottle()
        app.route('<t:path>', ['GET', 'POST'], make_view(self))
        return app

    def run(self, server=None, host=None,
            port=None, enable_pretty_logging=True):
        if enable_pretty_logging:
            from werobot.logger import enable_pretty_logging
            enable_pretty_logging(self.logger)
        if server is None:
            server = self.config["SERVER"]
        if host is None:
            host = self.config["HOST"]
        if port is None:
            port = self.config["PORT"]
        try:
            self.wsgi.run(server=server, host=host, port=port)
        except KeyboardInterrupt:
            exit(0)
