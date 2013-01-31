import werobot
import werobot.util
import werobot.test


def test_echo():
    robot = werobot.WeRoBot(token=werobot.util.generate_token())

    @robot.handler
    def report(message):
        x, y = message.location
        return 'You are at ({x}, {y})'.format(
            x=x,
            y=y
        )

    tester = werobot.test.WeTest(robot)
    message = werobot.test.make_location_message('20', '30', 40, 'label')
    assert tester.send(message) == 'You are at (20, 30)'
