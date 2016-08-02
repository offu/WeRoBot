# -*- coding: utf-8 -*-

import os
import time
import random
from werobot.utils import generate_token, get_signature
import sys


def test_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "django_test.settings")
    sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 '../werobot/tests/contrib/django_test/'))

    from django.test.utils import setup_test_environment
    setup_test_environment()
    from django.test.client import Client
    from werobot.parser import parse_xml, process_message
    import django

    try:
        django.setup()
    except AttributeError:
        # Django1.6 doesn't have django.setup()
        pass

    c = Client()

    token = 'TestDjango'
    timestamp = str(time.time())
    nonce = str(random.randint(0, 10000))
    signature = get_signature(token, timestamp, nonce)
    echostr = generate_token()

    response = c.get('/robot/', {'signature': signature,
                                 'timestamp': timestamp,
                                 'nonce': nonce,
                                 'echostr': echostr})
    assert response.status_code == 200
    assert response.content.decode('utf-8') == echostr

    xml = """
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[this is a test]]></Content>
        <MsgId>1234567890123456</MsgId>
    </xml>"""
    params = "?timestamp=%s&nonce=%s&signature=%s" % \
             (timestamp, nonce, signature)
    url = '/robot/'
    response = c.post(url,
                      data=xml,
                      content_type="text/xml")

    assert response.status_code == 403

    url += params
    response = c.post(url,
                      data=xml,
                      content_type="text/xml")

    assert response.status_code == 200
    response = process_message(parse_xml(response.content))
    assert response.content == 'hello'


def test_flask_and_tornado():
    from webtest import TestApp
    from webtest.app import AppError
    from werobot.contrib.flask import FlaskWeRoBot
    from flask import Flask
    from werobot.parser import process_message, parse_xml
    from tornado.wsgi import WSGIAdapter
    import tornado.web
    from werobot.contrib.tornado import make_handler

    token = 'TestFlask'
    timestamp = str(time.time())
    nonce = str(random.randint(0, 10000))
    signature = get_signature(token, timestamp, nonce)
    echostr = generate_token()

    apps = []

    app = Flask(__name__)
    robot = FlaskWeRoBot(enable_session=False,
                         token=token)

    @robot.text
    def hello():
        return 'hello'

    robot.init_app(app)
    app = TestApp(app)
    apps.append(app)

    handler = make_handler(robot)
    application = tornado.web.Application([
        (r"/robot/", handler),
    ])
    app = TestApp(WSGIAdapter(application))
    apps.append(app)

    params = "?timestamp=%s&nonce=%s&signature=%s&echostr=%s" % \
             (timestamp, nonce, signature, echostr)

    for app in apps:
        url = '/robot/' + params
        response = app.get(url)

        assert response.status_code == 200
        assert response.body.decode('utf-8') == echostr

        url = '/robot/'
        xml = """
                <xml>
                    <ToUserName><![CDATA[toUser]]></ToUserName>
                    <FromUserName><![CDATA[fromUser]]></FromUserName>
                    <CreateTime>1348831860</CreateTime>
                    <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[this is a test]]></Content>
                    <MsgId>1234567890123456</MsgId>
                </xml>"""
        try:
            app.post(url, xml, content_type="text/xml")
        except AppError:
            # WebTest will raise an AppError if the status_code is not >= 200 and < 400.
            pass

        url += params
        response = app.post(url, xml, content_type="text/xml")

        assert response.status_code == 200
        response = process_message(parse_xml(response.body))
        assert response.content == 'hello'
