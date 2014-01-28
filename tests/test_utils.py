# -*- coding: utf-8 -*-

import six

from werobot.utils import generate_token, check_token, to_text


def test_token_generator():
    assert not check_token('AA C')
    assert check_token(generate_token())


def test_to_text():
    assert to_text(5) == '5'
    if six.PY3:
        assert to_text(b'b') == 'b'
    else:
        assert to_text('喵') == unicode('喵'.decode('utf-8'))
