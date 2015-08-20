# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import base64
import socket
import struct

try:
    from Crypto.Cipher import AES
except ImportError:
    raise RuntimeError("You need to install PyCrypto.")

from . import pkcs7
from .exceptions import UnvalidEncodingAESKey, AppIdValidationError
from werobot.utils import to_text, to_binary, generate_token, byte2int


class PrpCrypto(object):
    """
    提供接收和推送给公众平台消息的加解密接口
    """
    def __init__(self, key):
        self.cipher = AES.new(key, AES.MODE_CBC, key[:16])

    def get_random_string(self):
        """
        :return: 长度为16的随即字符串
        """
        return generate_token(16)

    def encrypt(self, text, app_id):
        """
        对明文进行加密
        :param text: 需要加密的明文
        :param app_id: 微信公众平台的 AppID
        :return: 加密后的字符串
        """
        text = b"".join([
            self.get_random_string(),
            struct.pack(b"I", socket.htonl(len(text))),
            to_binary(text),
            to_binary(app_id)
        ])
        text = pkcs7.encode(text)

        ciphertext = to_binary(self.cipher.encrypt(text))
        return base64.b64encode(ciphertext)

    def decrypt(self, text, app_id):
        """
        对密文进行解密
        :param text: 需要解密的密文
        :param app_id: 微信公众平台的 AppID
        :return: 解密后的字符串
        """
        text = to_binary(text)
        plain_text = self.cipher.decrypt(base64.b64decode(text))

        padding = byte2int(plain_text, -1)
        content = plain_text[16:-padding]

        xml_len = socket.ntohl(struct.unpack("I", content[:4])[0])
        xml_content = content[4:xml_len+4]
        from_appid = content[xml_len+4:]

        if to_text(from_appid) != app_id:
            raise AppIdValidationError(text, app_id)

        return xml_content


class MessageCrypt(object):
    def __init__(self, token, encoding_aes_key, app_id):
        key = base64.b64decode(to_binary(encoding_aes_key + '='))
        if len(key) != 32:
            raise UnvalidEncodingAESKey(encoding_aes_key)
        self.prp_crypto = PrpCrypto(key)

        self.token = token
        self.app_id = app_id

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
