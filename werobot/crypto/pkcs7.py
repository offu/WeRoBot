# -*- coding: utf-8 -*-

from werobot.utils import to_binary

_BLOCK_SIZE = 32


def encode(text):
    # 计算需要填充的位数
    amount_to_pad = _BLOCK_SIZE - (len(text) % _BLOCK_SIZE)
    if not amount_to_pad:
        amount_to_pad = _BLOCK_SIZE
    # 获得补位所用的字符
    pad = chr(amount_to_pad)
    return text + to_binary(pad * amount_to_pad)


def decode(decrypted):
    pad = ord(decrypted[-1])
    if pad < 1 or pad > 32:
        pad = 0
    return decrypted[:-pad]
