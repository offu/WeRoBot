# -*- coding: utf-8 -*-

import six

from werobot.utils import generate_token, check_token, to_text, to_binary


def test_token_generator():
    assert not check_token('AA C')
    assert check_token(generate_token())


def test_to_text():
    assert to_text(6) == six.text_type(6)
    assert to_text(b"aa") == "aa"
    assert to_text("cc") == "cc"
    if six.PY2:
        assert to_text(u"喵") == u"喵"
        assert to_text("喵") == u"喵"


def test_to_binary():
    assert to_binary(6) == six.binary_type(6)
    assert to_binary(b"aa") == b"aa"
    assert to_binary("cc") == b"cc"
    if six.PY2:
        assert to_binary(u"喵") == "喵"
        assert to_binary("喵") == "喵"
