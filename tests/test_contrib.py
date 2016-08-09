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
                                 'django_test_env'))

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


def test_flask_bottle_and_tornado():
    from werobot import WeRoBot
    from webtest import TestApp
    from webtest.app import AppError
    from werobot.contrib.flask import make_view
    from werobot.contrib.bottle import make_view
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

    robot = WeRoBot(token=token, enable_session=False)

    @robot.text
    def hello():
        return 'hello'

    flask_app = Flask(__name__)
    flask_app.debug = True
    flask_app.add_url_rule(rule='/robot/',
                     endpoint='werobot',
                     view_func=make_view(robot),
                     methods=['GET', 'POST'])
    apps.append(flask_app)

    from bottle import Bottle
    from werobot.contrib.bottle import make_view

    bottle_app = Bottle()
    bottle_app.route(
        '/robot/',
        ['GET', 'POST'],
        make_view(robot)
    )
    apps.append(bottle_app)

    tornado_app = tornado.web.Application([
        (r"/robot/", make_handler(robot)),
    ])
    apps.append(WSGIAdapter(tornado_app))

    params = "?timestamp=%s&nonce=%s&signature=%s&echostr=%s" % \
             (timestamp, nonce, signature, echostr)

    for app in apps:
        url = '/robot/' + params
        response = TestApp(app).get(url)

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
            # WebTest will raise an AppError
            # if the status_code is not >= 200 and < 400.
            pass

        url += params
        response = app.post(url, xml, content_type="text/xml")

        assert response.status_code == 200
        response = process_message(parse_xml(response.body))
        assert response.content == 'hello'
