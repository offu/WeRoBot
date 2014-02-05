# -*- coding: utf-8 -*-

import six

from werobot.utils import generate_token, check_token, to_text


def test_token_generator():
    assert not check_token('AA C')
    assert check_token(generate_token())


def test_to_text():
    assert to_text("6") == 6
    assert to_text(six.binary_type("aa")) == six.text_type("aa")
    assert to_text(six.text_type("cc")) == six.text_type("cc")

