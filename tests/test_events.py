import werobot
import werobot.utils
import werobot.testing


def test_events():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())
    t = [False, '', 'NOTCHANGED']

    @robot.subscribe
    def first(message):
        return 'Hi'

    tester = werobot.testing.WeTest(robot)

    xml = """
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[subscribe]]></Event>
    </xml>
    """
    assert tester.send_xml(xml) == 'Hi', tester.send_xml(xml)

    @robot.unsubscribe
    def second(message):
        t[0] = True

    xml = """
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[unsubscribe]]></Event>
    </xml>
    """
    tester.send_xml(xml)
    assert t[0]

    @robot.click
    def f(message):
        t[1] = message.key

    xml = """
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[CLICK]]></Event>
        <EventKey><![CDATA[EVENTKEY]]></EventKey>
    </xml>
    """
    tester.send_xml(xml)
    assert t[1] == 'EVENTKEY'

    @robot.key_click('MYEVENT')
    def key(message):
        return message.key

    @robot.key_click('NOTMYEVENT')
    def nokey(message):
        t[2] = 'CHANGED'
        return message.key

    xml = """
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[CLICK]]></Event>
        <EventKey><![CDATA[MYEVENT]]></EventKey>
    </xml>
    """

    assert tester.send_xml(xml) == 'MYEVENT'
    assert t[2] == 'NOTCHANGED'

    @robot.key_click('ARGS')
    def key():
        return 'ARGS'

    xml = """
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[CLICK]]></Event>
        <EventKey><![CDATA[ARGS]]></EventKey>
    </xml>
    """
    assert tester.send_xml(xml) == 'ARGS'
