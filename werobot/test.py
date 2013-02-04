from . import WeRoBot
from .messages import WeChatMessage, TextMessage, ImageMessage, LocationMessage

__all__ = ['WeTest']


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
    message = TextMessage(
        'test',
        'test',
        0,
        content
    )
    return message


def make_image_message(img):
    message = ImageMessage(
        'test',
        'test',
        0,
        img
    )
    return message


def make_location_message(x, y, scale, label):
    message = LocationMessage(
        'test',
        'test',
        0,
        x,
        y,
        scale,
        label
    )
    return message
