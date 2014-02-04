# -*- coding:utf-8 -*-

from werobot.parser import parse_user_msg
from werobot.messages import EventMessage


def test_location_event():
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
    assert isinstance(message, EventMessage)
    assert message.type == "location"
    assert message.latitude == 23.137466
    assert message.longitude == 113.352425
    assert message.precision == 119.385040
