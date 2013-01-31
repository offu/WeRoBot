import werobot
import werobot.util
import werobot.test


def test_echo():
    robot = werobot.WeRoBot(token=werobot.util.generate_token())

    @robot.handler
    def echo(message):
        return message.content

    tester = werobot.test.WeTest(robot)
    message = werobot.test.make_text_message('test')
    assert tester.send(message) == 'test'
