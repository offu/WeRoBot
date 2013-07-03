import werobot
import werobot.utils
import werobot.testing


def test_echo():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())

    @robot.handler
    def echo(message):
        return message.img

    tester = werobot.testing.WeTest(robot)
    message = werobot.testing.make_image_message('http://a.com/b.jpg')
    assert tester.send(message) == 'http://a.com/b.jpg'
