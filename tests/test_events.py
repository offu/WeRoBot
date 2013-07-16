import werobot
import werobot.utils
import werobot.testing


def test_events():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())
    t = [False, '']

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
    assert tester.send_xml(xml) == 'Hi'

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
