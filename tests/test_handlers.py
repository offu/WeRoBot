from werobot import WeRoBot
from werobot.utils import generate_token
from werobot import testing, errors
from nose.tools import assert_raises


def make_essential():
    robot = WeRoBot(token=generate_token())
    tester = testing.WeTest(robot)
    return robot, tester


def test_errors():
    robot, tester = make_essential()

    with assert_raises(errors.HandlerNotFound):
        tester.send(testing.make_text_message('oo'))

    with assert_raises(errors.UnknownMessageType):
        message = testing.make_text_message('xx')
        message.type = 'html'
        tester.send(message)


def test_none():
    robot, tester = make_essential()

    @robot.text
    def first(message):
        pass

    message = testing.make_text_message('oo')
    assert tester.send(message) is None


def test_text():
    robot, tester = make_essential()

    @robot.text
    def first(message):
        if 'hi' in message.content:
            return 'Hello'
        else:
            return 'Hi'

    message = testing.make_text_message('oo')
    assert tester.send(message) == 'Hi'
    message = testing.make_text_message('hi')
    assert tester.send(message) == 'Hello'


def test_image():
    robot, tester = make_essential()

    image_url = 'http://a.com/b.jpg'

    @robot.image
    def first(message):
        return message.img

    message = testing.make_image_message(image_url)
    assert tester.send(message) == image_url


def test_location():
    robot, tester = make_essential()

    @robot.location
    def report(message):
        x, y = message.location
        return 'You are at ({x}, {y})'.format(
            x=x,
            y=y
        )

    message = testing.make_location_message('20', '30', 40, 'label')
    assert tester.send(message) == 'You are at (20, 30)'


def test_full_types():
    pass


#def test_():
    #robot, tester = make_essential()

    #@robot.
    #def first(message):
        #return

    #tester.send(message)
