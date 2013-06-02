# -*- coding: utf-8 -*-

import sys

py = sys.version_info
py3k = py >= (3, 0, 0)


from werobot.utils import generate_token, check_token, to_unicode


def test_token_generator():
    assert not check_token('AA C')
    assert check_token(generate_token())


def test_to_unicode():
    assert to_unicode(5) == '5'
    if py3k:
        assert to_unicode(b'b') == 'b'
    else:
        assert to_unicode('喵') == unicode('喵')
