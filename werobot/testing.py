from .messages import TextMessage, ImageMessage, LocationMessage
from .parser import parse_user_msg

__all__ = ['WeTest']
_kwargs = {
    'msgid': 1234567890123456,
    'touser': 'test',
    'fromuser': 'test',
    'time': 123456789,
}


class WeTest(object):
    def __init__(self, app):
        self._app = app

    def send(self, message):
        return self._app.get_reply(message)

    def send_xml(self, xml):
        message = parse_user_msg(xml)
        return self.send(message)


def make_text_message(content):
    message = TextMessage(content, **_kwargs)
    return message


def make_image_message(img):
    message = ImageMessage(img, **_kwargs)
    return message


def make_location_message(x, y, scale, label):
    message = LocationMessage(x, y, scale, label, **_kwargs)
    return message
