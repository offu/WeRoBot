from werobot.parser import parse_user_msg


def test_none_message():
    assert not parse_user_msg("")


def test_text_message():
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
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 1348831860
    assert message.type == "text"
    assert message.content == "this is a test"
    assert message.message_id == 1234567890123456


def test_image_message():
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
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 1348831860
    assert message.type == "image"
    assert message.img == "this is a url"
    assert message.message_id == 1234567890123456


def test_location_message():
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
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 1351776360
    assert message.type == "location"
    assert message.location == (23.134521, 113.358803)
    assert message.scale == 20
    assert message.label == "Location"
    assert message.message_id == 1234567890123456


def test_link_message():
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
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 1351776360
    assert message.type == "link"
    assert message.title == "WeRoBot"
    assert message.description == "Link to WeRoBot"
    assert message.url == "https://github.com/whtsky/WeRoBot"
    assert message.message_id == 1234567890123456


def test_voice_message():
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
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 1357290913
    assert message.type == "voice"
    assert message.media_id == "media_id"
    assert message.format == "Format"
    assert message.recognition == "Meow~"
    assert message.message_id == 1234567890123456


def test_unknown_message():
    xml = """
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
    """
    message = parse_user_msg(xml)
    assert message.raw == xml
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 1351776360


def test_subscribe_event():
    message = parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[subscribe]]></Event>
    </xml>
    """)
    assert message.target == "toUser"
    assert message.source == "FromUser"
    assert message.time == 123456789
    assert message.type == "subscribe_event"

    message = parse_user_msg("""
    <xml><ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[subscribe]]></Event>
        <EventKey><![CDATA[qrscene_123123]]></EventKey>
        <Ticket><![CDATA[TICKET]]></Ticket>
    </xml>
    """)
    assert message.target == "toUser"
    assert message.source == "FromUser"
    assert message.time == 123456789
    assert message.type == "subscribe_event"
    assert message.key == "qrscene_123123"
    assert message.ticket == "TICKET"


def test_unsubscribe_event():
    message = parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[unsubscribe]]></Event>
    </xml>
    """)
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 123456789
    assert message.type == "unsubscribe_event"


def test_scan_event():
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
    assert message.target == "toUser"
    assert message.source == "FromUser"
    assert message.time == 123456789
    assert message.type == "scan_event"
    assert message.key == "SCENE_VALUE"
    assert message.ticket == "TICKET"


def test_click_event():
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
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 123456789
    assert message.type == "click_event"
    assert message.key == "EVENTKEY"


def test_view_event():
    message = parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[VIEW]]></Event>
        <EventKey><![CDATA[www.qq.com]]></EventKey>
    </xml>""")
    assert message.target == "toUser"
    assert message.source == "FromUser"
    assert message.time == 123456789
    assert message.type == "view_event"
    assert message.key == "www.qq.com"


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
    assert message.target == "toUser"
    assert message.source == "fromUser"
    assert message.time == 123456789
    assert message.type == "location_event"
    assert message.latitude == 23.137466
    assert message.longitude == 113.352425
    assert message.precision == 119.385040


def test_template_send_job_finish_event():
    message = parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[gh_7f083739789a]]></ToUserName>
        <FromUserName><![CDATA[oia2TjuEGTNoeX76QEjQNrcURxG8]]></FromUserName>
        <CreateTime>1395658920</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[TEMPLATESENDJOBFINISH]]></Event>
        <MsgID>200163836</MsgID>
        <Status><![CDATA[success]]></Status>
    </xml>
    """)
    assert message.message_id == 200163836
    assert message.status == 'success'

    assert parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[gh_7f083739789a]]></ToUserName>
        <FromUserName><![CDATA[oia2TjuEGTNoeX76QEjQNrcURxG8]]></FromUserName>
        <CreateTime>1395658984</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[TEMPLATESENDJOBFINISH]]></Event>
        <MsgID>200163840</MsgID>
        <Status><![CDATA[failed: system failed]]></Status>
    </xml>
    """).status == 'failed: system failed'


def test_unknown_event():
    message = parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[unknown]]></Event>
    </xml>
    """)
    assert message.target == "toUser"
    assert message.source == "FromUser"
    assert message.time == 123456789
    assert message.type == "unknown_event"
