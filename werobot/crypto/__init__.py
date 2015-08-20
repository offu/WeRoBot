# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import base64

try:
    from Crypto.Cipher import AES
except ImportError:
    raise RuntimeError("You need to install PyCrypto.")

from . import pkcs7
from werobot.utils import to_binary


class PrpCrypto(object):
    def __init__(self, token, encoding_aes_key, app_id):
        pass

    def decrypt_message(self, timestamp, nonce, msg_signature, encrypt_msg):
        """
        解密收到的微信消息
        :param timestamp: 请求 URL 中收到的 timestamp
        :param nonce: 请求 URL 中收到的 nonce
        :param msg_signature: 请求 URL 中收到的 msg_signature
        :param encrypt_msg: 收到的加密文本. ( XML 中的 <Encrypt> 部分 )
        :return: 解密后的 XML 文本
        """
        pass

    def encrypt_message(self, reply):
        """
        加密微信回复
        :param reply: 加密前的回复
        :type reply: WeChatReply
        :return: 加密后的回复文本
        """
        pass
