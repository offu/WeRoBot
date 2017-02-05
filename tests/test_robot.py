# -*- coding:utf-8 -*-

import hashlib
import time
import six
import os
import pytest

from werobot import WeRoBot
from werobot.utils import generate_token, to_text


def test_signature_checker():
    token = generate_token()

    robot = WeRoBot(token, enable_session=False)

    timestamp = str(int(time.time()))
    nonce = '12345678'

    sign = [token, timestamp, nonce]
    sign.sort()
    sign = ''.join(sign)
    if six.PY3:
        sign = sign.encode()
    sign = hashlib.sha1(sign).hexdigest()

    assert robot.check_signature(timestamp, nonce, sign)


def test_register_handlers():
    robot = WeRoBot(enable_session=False)

    for type in robot.message_types:
        assert hasattr(robot, type) or \
               hasattr(robot, type.replace('_event', ''))

    @robot.text
    def text_handler():
        return "Hi"

    assert robot._handlers["text"] == [(text_handler, 0)]

    @robot.image
    def image_handler(message):
        return 'nice pic'

    assert robot._handlers["image"] == [(image_handler, 1)]

    assert robot.get_handlers("text") == [(text_handler, 0)]

    @robot.handler
    def handler(message, session):
        pass

    assert robot.get_handlers("text") == [(text_handler, 0), (handler, 2)]

    @robot.location
    def location_handler():
        pass

    assert robot._handlers["location"] == [(location_handler, 0)]

    @robot.link
    def link_handler():
        pass

    assert robot._handlers["link"] == [(link_handler, 0)]

    @robot.subscribe
    def subscribe_handler():
        pass

    assert robot._handlers["subscribe_event"] == [(subscribe_handler, 0)]

    @robot.unsubscribe
    def unsubscribe_handler():
        pass

    assert robot._handlers["unsubscribe_event"] == [(unsubscribe_handler, 0)]

    @robot.voice
    def voice_handler():
        pass

    assert robot._handlers["voice"] == [(voice_handler, 0)]

    @robot.click
    def click_handler():
        pass

    assert robot._handlers["click_event"] == [(click_handler, 0)]

    @robot.key_click("MENU")
    def menu_handler():
        pass

    assert len(robot._handlers["click_event"]) == 2


def test_filter():
    import re
    import werobot.testing
    robot = WeRoBot(enable_session=False)

    @robot.filter("喵")
    def _1():
        return "喵"

    assert len(robot._handlers["text"]) == 1

    @robot.filter(re.compile(to_text(".*?呵呵.*?")))
    def _2():
        return "哼"

    assert len(robot._handlers["text"]) == 2

    @robot.text
    def _3():
        return "汪"

    assert len(robot._handlers["text"]) == 3

    def _make_xml(content):
        return """
            <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1348831860</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            <MsgId>1234567890123456</MsgId>
            </xml>
        """ % content

    tester = werobot.testing.WeTest(robot)

    assert tester.send_xml(_make_xml("啊"))._args['content'] == u"汪"
    assert tester.send_xml(_make_xml("啊呵呵"))._args['content'] == u"哼"
    assert tester.send_xml(_make_xml("喵"))._args['content'] == u"喵"

    try:
        os.remove(os.path.abspath("werobot_session"))
    except OSError:
        pass
    robot = WeRoBot(enable_session=False)

    @robot.filter("帮助", "跪求帮助", re.compile(".*?help.*?"))
    def _():
        return "就不帮"

    assert len(robot._handlers["text"]) == 3

    @robot.text
    def _4():
        return "哦"

    assert len(robot._handlers["text"]) == 4

    tester = werobot.testing.WeTest(robot)

    assert tester.send_xml(_make_xml("啊"))._args['content'] == u"哦"
    assert tester.send_xml(_make_xml("帮助"))._args['content'] == u"就不帮"
    assert tester.send_xml(_make_xml("跪求帮助"))._args['content'] == u"就不帮"
    assert tester.send_xml(_make_xml("ooohelp"))._args['content'] == u"就不帮"


def test_register_not_callable_object():
    robot = WeRoBot(enable_session=False)
    with pytest.raises(ValueError):
        robot.add_handler("s")


def test_error_page():
    robot = WeRoBot()

    @robot.error_page
    def make_error_page(url):
        return url

    assert robot.make_error_page('喵') == '喵'


def test_config_ignore():
    from werobot.config import Config
    config = Config(
        TOKEN="token from config"
    )
    robot = WeRoBot(
        config=config,
        token="token2333"
    )
    assert robot.token == "token from config"
