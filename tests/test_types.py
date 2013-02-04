import werobot
import werobot.utils
import werobot.test


def test_types():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token())

    @robot.hello
    def first(message):
        return 'Hello'

    @robot.text
    def second(message):
        return "Hi"

    @robot.image
    def third(message):
        return 'nice pic'

    tester = werobot.test.WeTest(robot)
    message = werobot.test.make_text_message('oo')
    assert tester.send(message) == 'Hi'
    message = werobot.test.make_text_message('Hello2BizUser')
    assert tester.send(message) == 'Hello'
    message = werobot.test.make_image_message('img')
    assert tester.send(message) == 'nice pic'
