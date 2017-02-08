# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import base64
import socket
import struct
import time

try:
    from cryptography.hazmat.primitives.ciphers import \
        Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
except ImportError:  # pragma: no cover
    raise RuntimeError("You need to install Cryptography.")  # pragma: no cover

from . import pkcs7
from .exceptions import (
    UnvalidEncodingAESKey, AppIdValidationError, InvalidSignature
)
from werobot.utils import (
    to_text, to_binary, generate_token, byte2int, get_signature
)


class PrpCrypto(object):
    """
    提供接收和推送给公众平台消息的加解密接口
    """

    def __init__(self, key):
        key = to_binary(key)
        self.cipher = Cipher(algorithms.AES(key),
                             modes.CBC(key[:16]),
                             backend=default_backend())

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
            to_binary(self.get_random_string()),
            struct.pack(b"I", socket.htonl(len(to_binary(text)))),
            to_binary(text),
            to_binary(app_id)
        ])
        text = pkcs7.encode(text)
        encryptor = self.cipher.encryptor()
        ciphertext = to_binary(encryptor.update(text) + encryptor.finalize())
        return base64.b64encode(ciphertext)

    def decrypt(self, text, app_id):
        """
        对密文进行解密
        :param text: 需要解密的密文
        :param app_id: 微信公众平台的 AppID
        :return: 解密后的字符串
        """
        text = to_binary(text)
        decryptor = self.cipher.decryptor()
        plain_text = decryptor.update(
            base64.b64decode(text)) + decryptor.finalize()

        padding = byte2int(plain_text, -1)
        content = plain_text[16:-padding]

        xml_len = socket.ntohl(struct.unpack("I", content[:4])[0])
        xml_content = content[4:xml_len + 4]
        from_appid = content[xml_len + 4:]

        if to_text(from_appid) != app_id:
            raise AppIdValidationError(text, app_id)

        return xml_content


class MessageCrypt(object):
    ENCRYPTED_MESSAGE_XML = """
<xml>
<Encrypt><![CDATA[{encrypt}]]></Encrypt>
<MsgSignature><![CDATA[{signature}]]></MsgSignature>
<TimeStamp>{timestamp}</TimeStamp>
<Nonce><![CDATA[{nonce}]]></Nonce>
</xml>
    """.strip()

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
        signature = get_signature(self.token, timestamp, nonce, encrypt_msg)
        if signature != msg_signature:
            raise InvalidSignature(msg_signature)
        return self.prp_crypto.decrypt(encrypt_msg, self.app_id)

    def encrypt_message(self, reply, timestamp=None, nonce=None):
        """
        加密微信回复
        :param reply: 加密前的回复
        :type reply: WeChatReply 或 XML 文本
        :return: 加密后的回复文本
        """
        if hasattr(reply, "render"):
            reply = reply.render()

        timestamp = timestamp or to_text(int(time.time()))
        nonce = nonce or generate_token(5)
        encrypt = to_text(self.prp_crypto.encrypt(reply, self.app_id))
        signature = get_signature(self.token, timestamp, nonce, encrypt)
        return to_text(self.ENCRYPTED_MESSAGE_XML.format(
            encrypt=encrypt,
            signature=signature,
            timestamp=timestamp,
            nonce=nonce
        ))
