# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import pytest

from werobot.parser import process_message, parse_xml
from werobot.utils import generate_token, get_signature
import webtest
from webtest.app import AppError


@pytest.fixture
def wsgi_tester():
    def tester(app, token, endpoint):
        test_app = webtest.TestApp(app)

        response = test_app.get(endpoint, expect_errors=True)
        assert response.status_code == 403

        timestamp = str(time.time())
        nonce = str(random.randint(0, 10000))
        signature = get_signature(token, timestamp, nonce)
        echostr = generate_token()

        params = "?timestamp=%s&nonce=%s&signature=%s&echostr=%s" % (
            timestamp, nonce, signature, echostr
        )
        response = test_app.get(endpoint + params)

        assert response.status_code == 200
        assert response.body.decode('utf-8') == echostr

        response = test_app.get(endpoint, expect_errors=True)

        assert response.status_code == 403
        assert response.body.decode('utf-8') == u'喵'

        xml = """
                <xml>
                    <ToUserName><![CDATA[toUser]]></ToUserName>
                    <FromUserName><![CDATA[fromUser]]></FromUserName>
                    <CreateTime>1348831860</CreateTime>
                    <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[this is a test]]></Content>
                    <MsgId>1234567890123456</MsgId>
                </xml>
                """
        with pytest.raises(AppError):
            # WebTest will raise an AppError
            # if the status_code is not >= 200 and < 400.
            test_app.post(endpoint, xml, content_type="text/xml")

        response = test_app.post(endpoint + params, xml, content_type="text/xml")

        assert response.status_code == 200
        response = process_message(parse_xml(response.body))
        assert response.content == 'hello'

    return tester


@pytest.fixture(scope="module")
def hello_robot():
    from werobot import WeRoBot
    robot = WeRoBot(token='', enable_session=False)

    @robot.text
    def hello():
        return 'hello'

    @robot.error_page
    def make_error_page(url):
        return '喵'

    return robot


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

    client = Client()

    token = 'TestDjango'
    timestamp = str(time.time())
    nonce = str(random.randint(0, 10000))
    signature = get_signature(token, timestamp, nonce)
    echostr = generate_token()

    response = client.get('/robot/', {'signature': signature,
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
    response = client.post(url,
                           data=xml,
                           content_type="text/xml")

    assert response.status_code == 403
    assert response.content.decode('utf-8') == u'喵'

    url += params
    response = client.post(url,
                           data=xml,
                           content_type="text/xml")

    assert response.status_code == 200
    response = process_message(parse_xml(response.content))
    assert response.content == 'hello'

    response = client.options(url)
    assert response.status_code == 405


def test_flask(wsgi_tester, hello_robot):
    from flask import Flask
    from werobot.contrib.flask import make_view

    token = generate_token()
    endpoint = '/werobot_flask'

    hello_robot.token = token
    flask_app = Flask(__name__)
    flask_app.debug = True

    flask_app.add_url_rule(
        rule=endpoint,
        endpoint='werobot',
        view_func=make_view(hello_robot),
        methods=['GET', 'POST']
    )

    wsgi_tester(flask_app, token=token, endpoint=endpoint)


def test_bottle(wsgi_tester, hello_robot):
    from werobot.contrib.bottle import make_view
    from bottle import Bottle

    token = generate_token()
    endpoint = '/werobot_bottle'

    hello_robot.token = token

    bottle_app = Bottle()
    bottle_app.route(
        endpoint,
        ['GET', 'POST'],
        make_view(hello_robot)
    )

    wsgi_tester(bottle_app, token=token, endpoint=endpoint)


def test_tornado(wsgi_tester, hello_robot):
    from tornado.wsgi import WSGIAdapter
    import tornado.web
    from werobot.contrib.tornado import make_handler

    token = generate_token()
    endpoint = r'/werobot_tornado'
    hello_robot.token = token

    tornado_app = tornado.web.Application([
        (endpoint, make_handler(hello_robot)),
    ], debug=True)
    wsgi_tester(WSGIAdapter(tornado_app), token=token, endpoint=endpoint)


def test_werobot_wsgi(wsgi_tester, hello_robot):
    token = generate_token()
    endpoint = r'/rand'
    hello_robot.token = token

    wsgi_tester(hello_robot.wsgi, token=token, endpoint=endpoint)
