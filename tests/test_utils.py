# -*- coding: utf-8 -*-

import six

from werobot.utils import generate_token, check_token, to_text, to_binary
from werobot.utils import pay_sign_dict, make_error_page


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


def test_pay_sign_dict():
    appid = {"id": "nothing"}
    key = "test_key"

    pay_sign = pay_sign_dict(appid, key)

    assert "timestamp" in pay_sign[0]
    assert "noncestr" in pay_sign[0]
    assert "appid" in pay_sign[0]
    assert pay_sign[0]["appid"] == appid
    assert pay_sign[2] == u"SHA1"

    pay_sign = pay_sign_dict(appid, key,
                             add_noncestr=False,
                             add_timestamp=False,
                             gadd_appid=False)

    assert "timestamp" not in pay_sign[0]
    assert "noncestr" not in pay_sign[0]
    assert "appid" in pay_sign[0]


def test_make_error_page():
    rand_string = generate_token()
    content = make_error_page(rand_string)
    assert rand_string in content
