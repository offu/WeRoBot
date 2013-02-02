import werobot
import werobot.utils
import werobot.test


def test_one():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())

    @robot.handler
    def first(message):
        return

    @robot.handler
    def second(message):
        return "Hi"

    tester = werobot.test.WeTest(robot)
    message = werobot.test.make_text_message('oo')
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

    tester = werobot.test.WeTest(robot)
    message = werobot.test.make_text_message('oo')
    assert tester.send(message) == 'Hi'
    message = werobot.test.make_text_message('hi')
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

    tester = werobot.test.WeTest(robot)
    message = werobot.test.make_text_message('oo')
    assert tester.send(message) == 'txt'
    message = werobot.test.make_image_message('http://a.jpg')
    assert tester.send(message) == 'img'
