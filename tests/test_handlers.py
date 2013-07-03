import werobot
import werobot.utils
import werobot.testing


def test_one():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())

    @robot.handler
    def first(message):
        return

    def second(message):
        return "Hi"

    robot.add_handler(second)

    tester = werobot.testing.WeTest(robot)
    message = werobot.testing.make_text_message('oo')
    assert tester.send(message) == 'Hi'


def test_two():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())

    @robot.handler
    def first(message):
        if 'hi' in message.content:
            return 'Hello'

    @robot.handler
    def second(message):
        return "Hi"

    tester = werobot.testing.WeTest(robot)
    message = werobot.testing.make_text_message('oo')
    assert tester.send(message) == 'Hi'
    message = werobot.testing.make_text_message('hi')
    assert tester.send(message) == 'Hello'


def test_three():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())

    @robot.handler
    def first(message):
        if message.type == 'text':
            return 'txt'

    @robot.handler
    def second(message):
        if message.type == 'image':
            return 'img'

    tester = werobot.testing.WeTest(robot)
    message = werobot.testing.make_text_message('oo')
    assert tester.send(message) == 'txt'
    message = werobot.testing.make_image_message('http://a.jpg')
    assert tester.send(message) == 'img'


def test_add_handler():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())

    def a(message):
        pass

    robot.add_handler(a)

    try:
        robot.add_handler(5)
    except TypeError:
        pass
    else:
        raise
