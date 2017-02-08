# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
import random
import json
import six
import time
import io
import os

from hashlib import sha1
from functools import wraps

string_types = (six.string_types, six.text_type, six.binary_type)


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


def to_text(value, encoding="utf-8"):
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)


def to_binary(value, encoding="utf-8"):
    if isinstance(value, six.binary_type):
        return value
    if isinstance(value, six.text_type):
        return value.encode(encoding)
    return six.binary_type(value)


def is_string(value):
    return isinstance(value, string_types)


def byte2int(s, index=0):
    """Get the ASCII int value of a character in a string.

    :param s: a string
    :param index: the position of desired character

    :return: ASCII int value
    """
    if six.PY2:
        return ord(s[index])
    return s[index]


def generate_token(length=''):
    if not length:
        length = random.randint(3, 32)
    length = int(length)
    assert 3 <= length <= 32
    token = []
    letters = 'abcdefghijklmnopqrstuvwxyz' \
              'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
              '0123456789'
    for _ in range(length):
        token.append(random.choice(letters))
    return ''.join(token)


def json_loads(s):
    s = to_text(s)
    return json.loads(s)


def json_dumps(d):
    return json.dumps(d)


def pay_sign_dict(
        appid, pay_sign_key, add_noncestr=True,
        add_timestamp=True, add_appid=True, **kwargs
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

    _params = [(k.lower(), v)
               for k, v in kwargs.items()
               if k.lower() != "appid"]
    _params += [('appid', appid), ('appkey', pay_sign_key)]
    _params.sort()

    sign = '&'.join(["%s=%s" % (str(p[0]), str(p[1]))
                     for p in _params]).encode("utf-8")
    sign = sha1(sign).hexdigest()
    sign_type = 'SHA1'

    return dict(params), sign, sign_type


def make_error_page(url):
    with io.open(
            os.path.join(os.path.dirname(__file__), 'contrib/error.html'), 'r', encoding='utf-8'
    ) as error_page:
        return error_page.read().replace('{url}', url)
