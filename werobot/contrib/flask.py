# -*- coding: utf-8 -*-
from __future__ import absolute_import
from werobot.robot import BaseRoBot
from werobot.parser import parse_xml, process_message
from werobot.replies import process_function_reply
import logging
from flask import Flask


class WeRoBot(BaseRoBot):
    """
    给你的 Flask 应用添加 WeRoBot 支持。
    你可以在实例化 WeRoBot 的时候传入一个 Flask App 添加支持： ::
        app = Flask(__name__)
        robot = WeRoBot(app)
    或者也可以先实例化一个 WeRoBot ，然后通过 ``init_app`` 来给应用添加支持 ::
        robot = WeRoBot()
        def create_app():
            app = Flask(__name__)
            robot.init_app(app)
            return app

    """

    def __init__(self, app=None, endpoint='werobot', rule=None, *args, **kwargs):
        super(WeRoBot, self).__init__(*args, **kwargs)
        if app is not None:
            self.init_app(app, endpoint=endpoint, rule=rule)
        else:
            self.app = None

    def init_app(self, app, endpoint='werobot', rule=None):
        """
        为一个应用添加 WeRoBot 支持。
        如果你在实例化 ``WeRoBot`` 类的时候传入了一个 Flask App ，会自动调用本方法；
        否则你需要手动调用 ``init_app`` 来为应用添加支持。
        可以通过多次调用 ``init_app`` 并分别传入不同的 Flask App 来复用微信机器人。

        :param app: 一个标准的 Flask App。
        :param endpoint: WeRoBot 的 Endpoint 。默认为 ``werobot`` 。
            你可以通过 url_for(endpoint) 来获取到 WeRoBot 的地址。
            如果你想要在同一个应用中绑定多个 WeRoBot 机器人， 请使用不同的 endpoint .
        :param rule:
          WeRoBot 机器人的绑定地址。默认为 Flask App Config 中的 ``WEROBOT_ROLE``
        """
        assert isinstance(app, Flask)
        from werobot.utils import check_token

        self.app = app
        config = app.config
        token = self.token
        if token is None:
            token = config.setdefault('WEROBOT_TOKEN', 'none')
        if not check_token(token):
            raise AttributeError('%s is not a vailed WeChat Token.' % token)
        if rule is None:
            rule = config.setdefault('WEROBOT_ROLE', '/robot/')

        self.token = token

        from flask import request, make_response

        def handler():
            timestamp = request.args.get('timestamp', '')
            nonce = request.args.get('nonce', '')
            signature = request.args.get('signature', '')
            if not self.check_signature(
                    timestamp,
                    nonce,
                    signature,
            ):
                return 'Invalid Request.'
            if request.method == 'GET':
                return request.args['echostr']

            body = request.data
            message_dict = parse_xml(body)
            # Encrypt support
            if "Encrypt" in message_dict:
                xml = self.crypto.decrypt_message(
                    timestamp=timestamp,
                    nonce=nonce,
                    msg_signature=signature,
                    encrypt_msg=message_dict["Encrypt"]
                )
                message_dict = parse_xml(xml)

            message = process_message(message_dict)
            logging.info("Receive message %s" % message)
            reply = self.get_reply(message)
            if not reply:
                return ''
            # Encrypt support
            if self.use_encryption:
                response = make_response(
                    self.crypto.encrypt_message(reply))
            else:
                response = make_response(
                    process_function_reply(reply, message=message).render())
            response.headers['content_type'] = 'application/xml'
            return response

        app.add_url_rule(rule, endpoint=endpoint,
                         view_func=handler, methods=['GET', 'POST'])
