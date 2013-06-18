from werobot import WeRoBot
from werobot.utils import generate_token
from werobot import testing, errors
from nose.tools import assert_raises


def make_essential():
    robot = WeRoBot(token=generate_token())
    client = testing.WeTest(robot)
    return robot, client


def test_errors():
    robot, client = make_essential()

    with assert_raises(errors.HandlerNotFound):
        client.send(testing.make_text_message('oo'))

    with assert_raises(errors.UnknownMessageType):
        message = testing.make_text_message('xx')
        message.type = 'html'
        client.send(message)


def test_none():
    robot, client = make_essential()

    @robot.text
    def first(message):
        pass

    message = testing.make_text_message('oo')
    assert client.send(message) is None


def test_text():
    robot, client = make_essential()

    @robot.text
    def first(message):
        if 'hi' in message.content:
            return 'Hello'
        else:
            return 'Hi'

    message = testing.make_text_message('oo')
    assert client.send(message) == 'Hi'
    message = testing.make_text_message('hi')
    assert client.send(message) == 'Hello'


def test_image():
    robot, client = make_essential()

    image_url = 'http://a.com/b.jpg'

    @robot.image
    def first(message):
        return message.img

    message = testing.make_image_message(image_url)
    assert client.send(message) == image_url


def test_location():
    robot, client = make_essential()

    @robot.location
    def report(message):
        x, y = message.location
        return 'You are at ({x}, {y})'.format(
            x=x,
            y=y
        )

    message = testing.make_location_message('20', '30', 40, 'label')
    assert client.send(message) == 'You are at (20, 30)'


def test_full_types():
    pass


#def test_():
    #robot, client = make_essential()

    #@robot.
    #def first(message):
        #return

    #client.send(message)
