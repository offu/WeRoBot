import werobot
import werobot.utils
import werobot.testing


def test_echo():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())

    @robot.handler
    def echo(message):
        return message.content

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
    assert tester.send_xml(xml) == 'this is a test'
