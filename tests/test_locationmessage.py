import werobot
import werobot.utils
import werobot.testing


def test_echo():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())

    @robot.location
    def report(message):
        x, y = message.location
        return 'You are at ({x}, {y})'.format(
            x=x,
            y=y
        )

    tester = werobot.testing.WeTest(robot)
    xml = """
    <xml>
    <ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName><![CDATA[fromUser]]></FromUserName>
    <CreateTime>1351776360</CreateTime>
    <MsgType><![CDATA[location]]></MsgType>
    <Location_X>20.00000</Location_X>
    <Location_Y>30.00000</Location_Y>
    <Scale>40</Scale>
    <Label><![CDATA[label]]></Label>
    <MsgId>1234567890123456</MsgId>
    </xml>
    """
    assert tester.send_xml(xml) == 'You are at (20.0, 30.0)'
