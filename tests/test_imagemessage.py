import werobot
import werobot.util
import werobot.test


def test_echo():
    robot = werobot.WeRoBot(token=werobot.util.generate_token())

    @robot.handler
    def echo(message):
        return message.img

    tester = werobot.test.WeTest(robot)
    message = werobot.test.make_image_message('http://a.com/b.jpg')
    assert tester.send(message) == 'http://a.com/b.jpg'
