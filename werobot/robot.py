# -*- coding: utf-8 -*-

import warnings

from werobot.config import Config, ConfigAttribute
from werobot.client import Client
from werobot.exceptions import ConfigError
from werobot.parser import parse_xml, process_message
from werobot.replies import process_function_reply
from werobot.utils import (
    to_binary, to_text, check_signature, make_error_page, cached_property,
    is_regex
)

from inspect import signature

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
    """
    BaseRoBot 是整个应用的核心对象，负责提供 handler 的维护，消息和事件的处理等核心功能。

    :param logger: 用来输出 log 的 logger，如果是 ``None``，将使用 werobot.logger
    :param config: 用来设置的 :class:`werobot.config.Config` 对象 \\

    .. note:: 对于下面的参数推荐使用 :class:`~werobot.config.Config` 进行设置，\
    并且以下参数均已 **deprecated**。

    :param token: 微信公众号设置的 token **(deprecated)**
    :param enable_session: 是否开启 session **(deprecated)**
    :param session_storage: 用来储存 session 的对象，如果为 ``None``，\
    将使用 werobot.session.sqlitestorage.SQLiteStorage **(deprecated)**
    :param app_id: 微信公众号设置的 app id **(deprecated)**
    :param app_secret: 微信公众号设置的 app secret **(deprecated)**
    :param encoding_aes_key: 用来加解密消息的 aes key **(deprecated)**
    """
    message_types = [
        'subscribe_event',
        'unsubscribe_event',
        'click_event',
        'view_event',
        'scan_event',
        'scancode_waitmsg_event',
        'scancode_push_event',
        'pic_sysphoto_event',
        'pic_photo_or_album_event',
        'pic_weixin_event',
        'location_select_event',
        'location_event',
        'unknown_event',
        'user_scan_product_event',
        'user_scan_product_enter_session_event',
        'user_scan_product_async_event',
        'user_scan_product_verify_action_event',
        'card_pass_check_event',
        'card_not_pass_check_event',
        'user_get_card_event',
        'user_gifting_card_event',
        'user_del_card_event',
        'user_consume_card_event',
        'user_pay_from_pay_cell_event',
        'user_view_card_event',
        'user_enter_session_from_card_event',
        'update_member_card_event',
        'card_sku_remind_event',
        'card_pay_order_event',
        'templatesendjobfinish_event',
        'submit_membercard_user_info_event',  # event
        'text',
        'image',
        'link',
        'location',
        'voice',
        'unknown',
        'video',
        'shortvideo'
    ]

    token = ConfigAttribute("TOKEN")
    session_storage = ConfigAttribute("SESSION_STORAGE")

    def __init__(
        self,
        token=None,
        logger=None,
        enable_session=None,
        session_storage=None,
        app_id=None,
        app_secret=None,
        encoding_aes_key=None,
        config=None,
        **kwargs
    ):

        self._handlers = {k: [] for k in self.message_types}
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
        为每一条消息或事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='all')
        return f

    def text(self, f):
        """
        为文本 ``(text)`` 消息添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='text')
        return f

    def image(self, f):
        """
        为图像 ``(image)`` 消息添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='image')
        return f

    def location(self, f):
        """
        为位置 ``(location)`` 消息添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='location')
        return f

    def link(self, f):
        """
        为链接 ``(link)`` 消息添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='link')
        return f

    def voice(self, f):
        """
        为语音 ``(voice)`` 消息添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='voice')
        return f

    def video(self, f):
        """
        为视频 ``(video)`` 消息添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='video')
        return f

    def shortvideo(self, f):
        """
        为小视频 ``(shortvideo)`` 消息添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='shortvideo')
        return f

    def unknown(self, f):
        """
        为未知类型 ``(unknown)`` 消息添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='unknown')
        return f

    def subscribe(self, f):
        """
        为被关注 ``(subscribe)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='subscribe_event')
        return f

    def unsubscribe(self, f):
        """
        为被取消关注 ``(unsubscribe)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='unsubscribe_event')
        return f

    def click(self, f):
        """
        为自定义菜单事件 ``(click)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='click_event')
        return f

    def scan(self, f):
        """
        为扫描推送 ``(scan)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='scan_event')
        return f

    def scancode_push(self, f):
        """
        为扫描推送 ``(scancode_push)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='scancode_push_event')
        return f

    def scancode_waitmsg(self, f):
        """
        为扫描弹消息 ``(scancode_waitmsg)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='scancode_waitmsg_event')
        return f

    def pic_sysphoto(self, f):
        """
        为弹出系统拍照发图的事件推送 ``(pic_sysphoto_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='pic_sysphoto_event')
        return f

    def pic_photo_or_album(self, f):
        """
        为弹出拍照或者相册发图的事件推送 ``(pic_photo_or_album_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='pic_photo_or_album_event')
        return f

    def pic_weixin(self, f):
        """
        为弹出微信相册发图器的事件推送 ``(pic_weixin_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='pic_weixin_event')
        return f

    def location_select(self, f):
        """
        为弹出地理位置选择器的事件推送 ``(location_select_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='location_select_event')
        return f

    def location_event(self, f):
        """
        为上报位置 ``(location_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='location_event')
        return f

    def view(self, f):
        """
        为链接 ``(view)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='view_event')
        return f

    def user_scan_product(self, f):
        """
        为打开商品主页事件推送 ``(user_scan_product_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='user_scan_product_event')
        return f

    def user_scan_product_enter_session(self, f):
        """
        为进入公众号事件推送 ``(user_scan_product_enter_session_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='user_scan_product_enter_session_event')
        return f

    def user_scan_product_async(self, f):
        """
        为地理位置信息异步推送 ``(user_scan_product_async_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='user_scan_product_async_event')
        return f

    def user_scan_product_verify_action(self, f):
        """
        为商品审核结果推送 ``(user_scan_product_verify_action_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='user_scan_product_verify_action_event')
        return f

    def card_pass_check(self, f):
        """
        为生成的卡券通过审核 ``(card_pass_check_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='card_pass_check_event')
        return f

    def card_not_pass_check(self, f):
        """
        为生成的卡券未通过审核 ``(card_not_pass_check_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='card_not_pass_check_event')
        return f

    def user_get_card(self, f):
        """
        为用户领取卡券 ``(user_get_card_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='user_get_card_event')
        return f

    def user_gifting_card(self, f):
        """
        为用户转赠卡券 ``(user_gifting_card_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='user_gifting_card_event')
        return f

    def user_del_card(self, f):
        """
        为用户删除卡券 ``(user_del_card_event)``  事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='user_del_card_event')
        return f

    def user_consume_card(self, f):
        """
        为卡券被核销 ``(user_consume_card_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='user_consume_card_event')
        return f

    def user_pay_from_pay_cell(self, f):
        """
        为微信买单完成 ``(user_pay_from_pay_cell_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='user_pay_from_pay_cell_event')
        return f

    def user_view_card(self, f):
        """
        为用户进入会员卡 ``(user_view_card_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='user_view_card_event')
        return f

    def user_enter_session_from_card(self, f):
        """
        为用户卡券里点击查看公众号进入会话 ``(user_enter_session_from_card_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='user_enter_session_from_card_event')
        return f

    def update_member_card(self, f):
        """
        为用户的会员卡积分余额发生变动 ``(update_member_card_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='update_member_card_event')
        return f

    def card_sku_remind(self, f):
        """
        为某个card_id的初始库存数大于200且当前库存小于等于100 ``(card_sku_remind_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='card_sku_remind_event')
        return f

    def card_pay_order(self, f):
        """
        为券点发生变动 ``(card_pay_order_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='card_pay_order_event')
        return f

    def submit_membercard_user_info(self, f):
        """
        为用户通过一键激活的方式提交信息并点击激活或者用户修改会员卡信息 ``(submit_membercard_user_info_event)``
        事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='submit_membercard_user_info_event')
        return f

    def templatesendjobfinish_event(self, f):
        """在模版消息发送任务完成后，微信服务器会将是否送达成功作为通知，发送到开发者中心中填写的服务器配置地址中
        """
        self.add_handler(f, type='templatesendjobfinish_event')
        return f

    def unknown_event(self, f):
        """
        为未知类型 ``(unknown_event)`` 事件添加一个 handler 方法的装饰器。
        """
        self.add_handler(f, type='unknown_event')
        return f

    def key_click(self, key):
        """
        为自定义菜单 ``(click)`` 事件添加 handler 的简便方法。

        **@key_click('KEYNAME')** 用来为特定 key 的点击事件添加 handler 方法。
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
        为文本 ``(text)`` 消息添加 handler 的简便方法。

        使用 ``@filter("xxx")``, ``@filter(re.compile("xxx"))``
        或 ``@filter("xxx", "xxx2")`` 的形式为特定内容添加 handler。
        """
        def wraps(f):
            self.add_filter(func=f, rules=list(args))
            return f

        return wraps

    def add_handler(self, func, type='all'):
        """
        为 BaseRoBot 实例添加一个 handler。

        :param func: 要作为 handler 的方法。
        :param type: handler 的种类。
        :return: None
        """
        if not callable(func):
            raise ValueError("{} is not callable".format(func))

        self._handlers[type].append(
            (func, len(signature(func).parameters.keys()))
        )

    def get_handlers(self, type):
        return self._handlers.get(type, []) + self._handlers['all']

    def add_filter(self, func, rules):
        """
        为 BaseRoBot 添加一个 ``filter handler``。

        :param func: 如果 rules 通过，则处理该消息的 handler。
        :param rules: 一个 list，包含要匹配的字符串或者正则表达式。
        :return: None
        """
        if not callable(func):
            raise ValueError("{} is not callable".format(func))
        if not isinstance(rules, list):
            raise ValueError("{} is not list".format(rules))
        if len(rules) > 1:
            for x in rules:
                self.add_filter(func, [x])
        else:
            target_content = rules[0]
            if isinstance(target_content, str):
                target_content = to_text(target_content)

                def _check_content(message):
                    return message.content == target_content
            elif is_regex(target_content):

                def _check_content(message):
                    return target_content.match(message.content)
            else:
                raise TypeError("%s is not a valid rule" % target_content)
            argc = len(signature(func).parameters.keys())

            @self.text
            def _f(message, session=None):
                _check_result = _check_content(message)
                if _check_result:
                    if isinstance(_check_result, bool):
                        _check_result = None
                    return func(*[message, session, _check_result][:argc])

    def parse_message(
        self, body, timestamp=None, nonce=None, msg_signature=None
    ):
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
        根据 message 的内容获取 Reply 对象。

        :param message: 要处理的 message
        :return: 获取的 Reply 对象
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
            self.logger.exception("Catch an exception")

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
            self.logger.warning("No handler responded message %s" % message)
            return ''
        if self.use_encryption:
            return self.crypto.encrypt_message(reply)
        else:
            return reply.render()

    def check_signature(self, timestamp, nonce, signature):
        """
        根据时间戳和生成签名的字符串 (nonce) 检查签名。

        :param timestamp: 时间戳
        :param nonce: 生成签名的随机字符串
        :param signature: 要检查的签名
        :return: 如果签名合法将返回 ``True``，不合法将返回 ``False``
        """
        return check_signature(
            self.config["TOKEN"], timestamp, nonce, signature
        )

    def error_page(self, f):
        """
        为 robot 指定 Signature 验证不通过时显示的错误页面。

        Usage::

            @robot.error_page
            def make_error_page(url):
                return "<h1>喵喵喵 %s 不是给麻瓜访问的快走开</h1>" % url

        """
        self.make_error_page = f
        return f


class WeRoBot(BaseRoBot):
    """
    WeRoBot 是一个继承自 BaseRoBot 的对象，在 BaseRoBot 的基础上使用了 bottle 框架，
    提供接收微信服务器发来的请求的功能。
    """
    @cached_property
    def wsgi(self):
        if not self._handlers:
            raise RuntimeError('No Handler.')
        from bottle import Bottle
        from werobot.contrib.bottle import make_view

        app = Bottle()
        app.route('<t:path>', ['GET', 'POST'], make_view(self))
        return app

    def run(
        self, server=None, host=None, port=None, enable_pretty_logging=True
    ):
        """
        运行 WeRoBot。

        :param server: 传递给 Bottle 框架 run 方法的参数，详情见\
        `bottle 文档 <https://bottlepy.org/docs/dev/deployment.html#switching-the-server-backend>`_
        :param host: 运行时绑定的主机地址
        :param port: 运行时绑定的主机端口
        :param enable_pretty_logging: 是否开启 log 的输出格式优化
        """
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
