# -*- coding: utf-8 -*-

from werobot.crypto import PrpCrypto, MessageCrypt
from werobot.utils import generate_token, to_binary, to_text
from werobot.parser import parse_xml
import time


def test_prpcrypto():
    key = "ReUrr0NKeHkppBQq"

    assert len(key) == 16

    crypto = PrpCrypto(key)
    text = generate_token(32)
    app_id = generate_token(32)
    assert crypto.decrypt(crypto.encrypt(text, app_id),
                          app_id) == to_binary(text)


def test_message_crypt():
    encoding_aes_key = generate_token(32) + generate_token(11)
    token = generate_token()
    timestamp = to_text(int(time.time()))
    nonce = generate_token(5)
    app_id = generate_token(18)
    crypt = MessageCrypt(token=token,
                         encoding_aes_key=encoding_aes_key,
                         app_id=app_id)

    message = crypt.encrypt_message('hello', timestamp, nonce)
    assert message is not None
    message = parse_xml(message)
    assert message is not None
    message = crypt.decrypt_message(message['TimeStamp'],
                                    message['Nonce'],
                                    message['MsgSignature'],
                                    message['Encrypt'])
    assert message == to_binary('hello')
