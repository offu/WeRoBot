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
    message = werobot.testing.make_location_message('20', '30', 40, 'label')
    assert tester.send(message) == 'You are at (20.0, 30.0)'
