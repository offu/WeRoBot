import hashlib
import time

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
    sign = hashlib.sha1(sign).hexdigest()

    assert robot.check_signature(timestamp, nonce, sign)
