# -*- coding: utf-8 -*-

from . import WeRoBot
from .messages import WeChatMessage, TextMessage, ImageMessage, LocationMessage

__all__ = ['WeTest']
_kwargs = {
    'msgid': 1234567890123456,
    'touser': 'test',
    'fromuser': 'test',
    'time': 123456789,
}


class WeTest(object):
    def __init__(self, app):
        if not isinstance(app, WeRoBot):
            raise TypeError
        self._app = app

    def send(self, message):
        if not isinstance(message, WeChatMessage):
            raise TypeError
        return self._app._get_reply(message)


def make_text_message(content):
    message = TextMessage(content, **_kwargs)
    return message


def make_image_message(img):
    message = ImageMessage(img, **_kwargs)
    return message


def make_location_message(x, y, scale, label):
    message = LocationMessage(x, y, scale, label, **_kwargs)
    return message
