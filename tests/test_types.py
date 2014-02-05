import werobot
import werobot.utils


def test_types():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())

    for type in robot.message_types:
        assert hasattr(robot, type)

    @robot.text
    def text_handler(message):
        return "Hi"

    assert robot._handlers["text"] == [text_handler]

    @robot.image
    def image_handler(message):
        return 'nice pic'

    assert robot._handlers["image"] == [image_handler]
