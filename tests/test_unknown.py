import werobot
import werobot.utils
import werobot.test


def test_link():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())

    tester = werobot.test.WeTest(robot)

    xml = """
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[..>_<]]></MsgType>
    </xml>
    """

    @robot.unknown
    def first(message):
        assert message.content == xml

    tester.send_xml(xml)
