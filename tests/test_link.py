import werobot
import werobot.utils
import werobot.test


def test_link():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())

    @robot.link
    def first(message):
        assert message.title == 'title'
        assert message.description == 'description'
        assert message.url == 'url'

    tester = werobot.test.WeTest(robot)

    xml = """
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[link]]></MsgType>
        <Title><![CDATA[title]]></Title>
        <Description><![CDATA[description]]></Description>
        <Url><![CDATA[url]]></Url>
    </xml>
    """
    tester.send_xml(xml)
