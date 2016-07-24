# -*- coding: utf-8 -*-

from werobot.crypto import PrpCrypto
from werobot.utils import generate_token, to_binary


def test_prpcrypto():
    key = "ReUrr0NKeHkppBQq"

    assert len(key) == 16

    crypto = PrpCrypto(key)
    text = generate_token(32)
    app_id = generate_token(32)
    assert crypto.decrypt(crypto.encrypt(text, app_id),
                          app_id) == to_binary(text)
