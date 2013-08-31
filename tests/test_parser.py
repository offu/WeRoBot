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
    assert message.target == 'toUser'
    assert message.source == 'fromUser'
    assert message.time == 1348831860
    assert message.type == 'text'
    assert message.content == 'this is a test'
    #assert message.id == 1234567890123456


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
    assert message.target == 'toUser'
    assert message.source == 'fromUser'
    assert message.time == 1348831860
    assert message.type == 'image'
    assert message.img == 'this is a url'


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
    assert message.target == 'toUser'
    assert message.source == 'fromUser'
    assert message.time == 1351776360
    assert message.type == 'location'
    assert message.location == (23.134521, 113.358803)
    assert message.scale == 20
    assert message.label == 'Location'


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
    assert message.target == 'toUser'
    assert message.source == 'fromUser'
    assert message.time == 1351776360
    assert message.type == 'link'
    assert message.title == 'WeRoBot'
    assert message.description == 'Link to WeRoBot'
    assert message.url == 'https://github.com/whtsky/WeRoBot'


def test_event_message():
    message = parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[subscribe]]></Event>
    </xml>
    """)
    assert message.target == 'toUser'
    assert message.source == 'fromUser'
    assert message.time == 123456789
    assert message.type == 'subscribe'

    message = parse_user_msg("""
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[unsubscribe]]></Event>
    </xml>
    """)
    assert message.type == 'unsubscribe'

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
    assert message.type == 'click'
    assert message.key == 'EVENTKEY'


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
