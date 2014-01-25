import werobot
import werobot.utils
import werobot.testing


def test_one():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())

    @robot.handler
    def first(message):
        return

    def second(message):
        assert message.time == 1348831860
        return "Hi"

    robot.add_handler(second)

    tester = werobot.testing.WeTest(robot)
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
    assert tester.send_xml(xml) == 'Hi'


def test_two():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())

    @robot.handler
    def first(message):
        if 'hi' in message.content:
            return 'Hello'

    @robot.handler
    def second(message):
        return "Hi"

    tester = werobot.testing.WeTest(robot)
    xml = """
    <xml>
    <ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName><![CDATA[fromUser]]></FromUserName>
    <CreateTime>1348831860</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[hi]]></Content>
    <MsgId>1234567890123456</MsgId>
    </xml>
    """
    assert tester.send_xml(xml) == 'Hi'
    xml = """
    <xml>
    <ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName><![CDATA[fromUser]]></FromUserName>
    <CreateTime>1348831860</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[heee]]></Content>
    <MsgId>1234567890123456</MsgId>
    </xml>
    """
    assert tester.send_xml(xml) == 'Hello'
