# -*- coding: utf-8 -*-

from werobot import WeRoBot
from werobot.parser import parse_user_msg
from werobot.replies import TextReply
import os

werobot = WeRoBot(enable_session=False)


def teardown_module(module):
    try:
        os.remove(os.path.abspath("werobot_session"))
    except OSError:
        pass


def test_subscribe_handler():
    @werobot.subscribe
    def subscribe(message):
        return '关注'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[subscribe]]></Event>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'关注'


def test_unsubscribe_handler():
    @werobot.unsubscribe
    def unsubscribe(message):
        return '取消关注'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[unsubscribe]]></Event>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'取消关注'


def test_scan_handler():
    @werobot.scan
    def scan(message):
        return '扫描'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[SCAN]]></Event>
            <EventKey><![CDATA[SCENE_VALUE]]></EventKey>
            <Ticket><![CDATA[TICKET]]></Ticket>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'扫描'


def test_click_handler():
    @werobot.click
    def scan(message):
        return '喵喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[CLICK]]></Event>
            <EventKey><![CDATA[EVENTKEY]]></EventKey>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'喵喵'


def test_view_handler():
    @werobot.view
    def view(message):
        return '汪汪'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[VIEW]]></Event>
            <EventKey><![CDATA[www.qq.com]]></EventKey>
        </xml>""")

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'汪汪'


def test_location_event_handler():
    @werobot.location_event
    def location_event(message):
        return '位置喵喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[LOCATION]]></Event>
            <Latitude>23.137466</Latitude>
            <Longitude>113.352425</Longitude>
            <Precision>119.385040</Precision>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'位置喵喵'


def test_unknown_event():
    @werobot.unknown_event
    def unknown_event(message):
        return '不知道的事件喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>123456789</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[unknown]]></Event>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'不知道的事件喵'


def test_text():
    @werobot.text
    def text(message):
        return '普通的Text喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1348831860</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[this is a test]]></Content>
            <MsgId>1234567890123456</MsgId>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'普通的Text喵'


def test_image():
    @werobot.image
    def image(message):
        return '图片喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1348831860</CreateTime>
            <MsgType><![CDATA[image]]></MsgType>
            <PicUrl><![CDATA[this is a url]]></PicUrl>
            <MsgId>1234567890123456</MsgId>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'图片喵'


def test_location():
    @werobot.location
    def location(message):
        return '地理位置汪'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1351776360</CreateTime>
            <MsgType><![CDATA[location]]></MsgType>
            <Location_X>23.134521</Location_X>
            <Location_Y>113.358803</Location_Y>
            <Scale>20</Scale>
            <Label><![CDATA[Location]]></Label>
            <MsgId>1234567890123456</MsgId>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'地理位置汪'


def test_link():
    @werobot.link
    def link(message):
        return '链接喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1351776360</CreateTime>
            <MsgType><![CDATA[link]]></MsgType>
            <Title><![CDATA[WeRoBot]]></Title>
            <Description><![CDATA[Link to WeRoBot]]></Description>
            <Url><![CDATA[https://github.com/whtsky/WeRoBot]]></Url>
            <MsgId>1234567890123456</MsgId>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'链接喵'


def test_voice():
    @werobot.voice
    def voice(message):
        return '声音喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1357290913</CreateTime>
            <MsgType><![CDATA[voice]]></MsgType>
            <MediaId><![CDATA[media_id]]></MediaId>
            <Format><![CDATA[Format]]></Format>
            <Recognition><![CDATA[Meow~]]></Recognition>
            <MsgId>1234567890123456</MsgId>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'声音喵'


def test_unknown():
    @werobot.unknown
    def unknown(message):
        return '不知道喵'

    message = parse_user_msg("""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1351776360</CreateTime>
            <MsgType><![CDATA[unknown]]></MsgType>
            <Title><![CDATA[WeRoBot]]></Title>
            <Description><![CDATA[Link to WeRoBot]]></Description>
            <Url><![CDATA[https://github.com/whtsky/WeRoBot]]></Url>
            <MsgId>1234567890123456</MsgId>
        </xml>
        """)

    reply = werobot.get_reply(message)

    assert isinstance(reply, TextReply)
    assert reply._args['content'] == u'不知道喵'
