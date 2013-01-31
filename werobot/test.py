from . import WeRoBot
from .messages import WeChatMessage, TextMessage

__all__ = ['WeTest']


class WeTest(object):
    def __init__(self, app):
        if not isinstance(app, WeRoBot):
            raise TypeError
        self._app = app

    def send(self, message):
        if not isinstance(message, WeChatMessage):
            raise TypeError
        for handler in self._app._handlers:
            reply = handler(message)
            if reply:
                return reply


def make_text_message(content):
    message = TextMessage(
        'test',
        'test',
        0,
        content
    )
    return message