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


def test_register_handlerss():
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


@raises(ValueError)
def test_register_not_callable_object():
    robot = WeRoBot()
    robot.add_handler("s")
