import werobot
import werobot.utils
import werobot.testing


def test_echo():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())

    @robot.handler
    def echo(message):
        return message.content

    tester = werobot.testing.WeTest(robot)
    message = werobot.testing.make_text_message('test')
    assert tester.send(message) == 'test'
