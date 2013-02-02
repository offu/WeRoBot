# -*- coding: utf-8 -*-
import werobot.reply
import werobot.test
from werobot.utils import to_unicode


def test_text_render():
    message = werobot.test.make_text_message('test')
    reply = werobot.reply.TextReply(message, content='hello', time=1359803261)
    reply_message = """
    <xml>
    <ToUserName><![Cmessage[test]]></ToUserName>
    <FromUserName><![Cmessage[test]]></FromUserName>
    <CreateTime>1359803261</CreateTime>
    <MsgType><![Cmessage[text]]></MsgType>
    <Content><![Cmessage[hello]]></Content>
    <FuncFlag>0</FuncFlag>
    </xml>
    """.strip().replace(" ", "").replace("\n", "")
    result = reply.render().strip().replace(" ", "").replace("\n", "")
    assert isinstance(result, unicode)
    assert result == to_unicode(reply_message)
