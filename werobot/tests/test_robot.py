import hashlib
import time
import six

from nose.tools import raises
from werobot import WeRoBot
from werobot.utils import generate_token


def test_signature_checker():
    token = generate_token()

    robot = WeRoBot(token)

    timestamp = str(int(time.time()))
    nonce = '12345678'

    sign = [token, timestamp, nonce]
    sign.sort()
    sign = ''.join(sign)
    if six.PY3:
        sign = sign.encode()
    sign = hashlib.sha1(sign).hexdigest()

    assert robot.check_signature(timestamp, nonce, sign)


def test_register_handlers():
    robot = WeRoBot()

    for type in robot.message_types:
        assert hasattr(robot, type)

    @robot.text
    def text_handler():
        return "Hi"

    assert robot._handlers["text"] == [(text_handler, 0)]

    @robot.image
    def image_handler(message):
        return 'nice pic'

    assert robot._handlers["image"] == [(image_handler, 1)]

    assert robot.get_handlers("text") == [(text_handler, 0)]

    @robot.handler
    def handler(message, session):
        pass

    assert robot.get_handlers("text") == [(text_handler, 0), (handler, 2)]

    @robot.location
    def location_handler():
        pass

    assert robot._handlers["location"] == [(location_handler, 0)]


    @robot.link
    def link_handler():
        pass
    
    assert robot._handlers["link"] == [(link_handler, 0)]

    @robot.subscribe
    def subscribe_handler():
        pass

    assert robot._handlers["subscribe"] == [(subscribe_handler, 0)]

    @robot.unsubscribe
    def unsubscribe_handler():
        pass

    assert robot._handlers["unsubscribe"] == [(unsubscribe_handler, 0)]

    @robot.voice
    def voice_handler():
        pass

    assert robot._handlers["voice"] == [(voice_handler, 0)]

    @robot.click
    def click_handler():
        pass

    assert robot._handlers["click"] == [(click_handler, 0)]

    @robot.key_click("MENU")
    def menu_handler():
        pass

    assert len(robot._handlers["click"]) == 2


@raises(ValueError)
def test_register_not_callable_object():
    robot = WeRoBot()
    robot.add_handler("s")
