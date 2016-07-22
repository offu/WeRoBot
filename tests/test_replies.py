# -*- coding:utf-8 -*-

import time
from werobot.parser import parse_user_msg
from werobot.replies import TextReply, ImageReply, MusicReply
from werobot.replies import TransferCustomerServiceReply, SuccessReply


def test_text_reply():
    message = parse_user_msg("""
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <PicUrl><![CDATA[this is a url]]></PicUrl>
        <MediaId><![CDATA[media_id]]></MediaId>
        <MsgId>1234567890123456</MsgId>
        </xml>
    """)
    t = int(time.time())
    reply = TextReply(message=message, content="aa", time=t)
    reply.render().strip() == """
    <xml>
    <ToUserName><![CDATA[fromUser]]></ToUserName>
    <FromUserName><![CDATA[toUser]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[aa]]></Content>
    </xml>""".format(time=t).strip()


def test_image_reply():
    message = parse_user_msg("""
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <PicUrl><![CDATA[this is a url]]></PicUrl>
        <MediaId><![CDATA[media_id]]></MediaId>
        <MsgId>1234567890123456</MsgId>
        </xml>
    """)
    t = int(time.time())
    reply = ImageReply(message=message, media_id="fdasfdasfasd", time=t)
    reply.render().strip() == """
    <xml>
    <ToUserName><![CDATA[fromUser]]></ToUserName>
    <FromUserName><![CDATA[toUser]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[image]]></MsgType>
    <Image>
    <MediaId><![CDATA[fdasfdasfasd]]></MediaId>
    </Image>
    </xml>""".format(time=t).strip()


def test_music_reply():
    t = int(time.time())
    reply = MusicReply(
        target='tg',
        source='ss',
        time=t,
        title='tt',
        description='ds',
        url='u1',
        hq_url='u2',
    )
    assert reply.render().strip() == """
    <xml>
    <ToUserName><![CDATA[tg]]></ToUserName>
    <FromUserName><![CDATA[ss]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[music]]></MsgType>
    <Music>
    <Title><![CDATA[tt]]></Title>
    <Description><![CDATA[ds]]></Description>
    <MusicUrl><![CDATA[u1]]></MusicUrl>
    <HQMusicUrl><![CDATA[u2]]></HQMusicUrl>
    </Music>
    </xml>""".format(time=t).strip()


def test_transfer_customer_service_reply():
    t = int(time.time())
    reply = TransferCustomerServiceReply(
        source='aaa',
        target='bbb',
        time=t
    )
    assert reply.render().strip() == """
    <xml>
    <ToUserName><![CDATA[bbb]]></ToUserName>
    <FromUserName><![CDATA[aaa]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[transfer_customer_service]]></MsgType>
    </xml>
    """.format(time=t).strip()


def test_success_reply():
    assert SuccessReply().render() == "success"
