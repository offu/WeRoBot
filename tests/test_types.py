import werobot
import werobot.utils
import werobot.testing


def test_types():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())

    for type in robot.message_types:
        assert hasattr(robot, type)

    @robot.text
    def second(message):
        return "Hi"

    @robot.image
    def third(message):
        return 'nice pic'

    tester = werobot.testing.WeTest(robot)
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
    assert tester.send_xml(xml) == 'Hi'
    xml = """
    <xml>
    <ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName><![CDATA[fromUser]]></FromUserName>
    <CreateTime>1348831860</CreateTime>
    <MsgType><![CDATA[image]]></MsgType>
    <PicUrl><![CDATA[this is a url]]></PicUrl>
    <MediaId><![CDATA[media_id]]></MediaId>
    <MsgId>1234567890123456</MsgId>
    </xml>
    """
    assert tester.send_xml(xml) == 'nice pic'
