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
    message = werobot.testing.make_text_message('oo')
    assert tester.send(message) == 'Hi'
    message = werobot.testing.make_image_message('img')
    assert tester.send(message) == 'nice pic'
