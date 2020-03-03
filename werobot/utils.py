# -*- coding: utf-8 -*-

import io
import json
import os
import random
import re
import string
import time
from functools import wraps
from hashlib import sha1

try:
    from secrets import choice
except ImportError:
    from random import choice

string_types = (str, bytes)

re_type = type(re.compile("regex_test"))


def get_signature(token, timestamp, nonce, *args):
    sign = [token, timestamp, nonce] + list(args)
    sign.sort()
    sign = to_binary(''.join(sign))
    return sha1(sign).hexdigest()


def check_signature(token, timestamp, nonce, signature):
    if not (token and timestamp and nonce and signature):
        return False
    sign = get_signature(token, timestamp, nonce)
    return sign == signature


def check_token(token):
    return re.match('^[A-Za-z0-9]{3,32}$', token)


def cached_property(method):
    prop_name = '_{}'.format(method.__name__)

    @wraps(method)
    def wrapped_func(self, *args, **kwargs):
        if not hasattr(self, prop_name):
            setattr(self, prop_name, method(self, *args, **kwargs))
        return getattr(self, prop_name)

    return property(wrapped_func)


def to_text(value, encoding="utf-8") -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        return value.decode(encoding)
    return str(value)


def to_binary(value, encoding="utf-8") -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode(encoding)
    return bytes(value)


def is_string(value) -> bool:
    """Check if value's type is `str` or `bytes`
    """
    return isinstance(value, string_types)


def byte2int(s, index=0):
    """Get the ASCII int value of a character in a string.

    :param s: a string
    :param index: the position of desired character

    :return: ASCII int value
    """
    return s[index]


def generate_token(length=''):
    if not length:
        length = random.randint(3, 32)
    length = int(length)
    assert 3 <= length <= 32
    letters = string.ascii_letters + string.digits
    return ''.join(choice(letters) for _ in range(length))


def json_loads(s):
    s = to_text(s)
    return json.loads(s)


def json_dumps(d):
    return json.dumps(d)


def pay_sign_dict(
    appid,
    pay_sign_key,
    add_noncestr=True,
    add_timestamp=True,
    add_appid=True,
    **kwargs
):
    """
    支付参数签名
    """
    assert pay_sign_key, "PAY SIGN KEY IS EMPTY"

    if add_appid:
        kwargs.update({'appid': appid})

    if add_noncestr:
        kwargs.update({'noncestr': generate_token()})

    if add_timestamp:
        kwargs.update({'timestamp': int(time.time())})

    params = kwargs.items()

    _params = [
        (k.lower(), v) for k, v in kwargs.items() if k.lower() != "appid"
    ]
    _params += [('appid', appid), ('appkey', pay_sign_key)]
    _params.sort()

    sign = '&'.join(["%s=%s" % (str(p[0]), str(p[1]))
                     for p in _params]).encode("utf-8")
    sign = sha1(sign).hexdigest()
    sign_type = 'SHA1'

    return dict(params), sign, sign_type


def make_error_page(url):
    with io.open(
        os.path.join(os.path.dirname(__file__), 'contrib/error.html'),
        'r',
        encoding='utf-8'
    ) as error_page:
        return error_page.read().replace('{url}', url)


def is_regex(value):
    return isinstance(value, re_type)
