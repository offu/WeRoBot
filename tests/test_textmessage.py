import werobot
import werobot.utils
import werobot.test


def test_echo():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())

    @robot.handler
    def echo(message):
        return message.content

    tester = werobot.test.WeTest(robot)
    message = werobot.test.make_text_message('test')
    print tester.send(message)
    assert tester.send(message) == 'test'
