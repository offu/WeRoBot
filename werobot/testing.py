from copy import deepcopy

from .messages import TextMessage, ImageMessage, LocationMessage, VoiceMessage
from .parser import parse_user_msg

__all__ = ['WeTest']
message_temple = {
    'msgid': 1234567890123456,
    'ToUserName': 'test',
    'FromUserName': 'test',
    'CreateTime': 123456789,
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
    message = deepcopy(message_temple)
    message["content"] = content
    message = TextMessage(message)
    return message


def make_image_message(img):
    message = deepcopy(message_temple)
    message["img"] = img
    message = ImageMessage(message)
    return message


def make_location_message(x, y, scale, label):
    message = deepcopy(message_temple)
    message["x"] = x
    message["y"] = y
    message["scale"] = scale
    message["label"] = label
    message = LocationMessage(message)
    return message


def make_voice_message(media_id, format, recognition):
    message = deepcopy(message_temple)
    message["media_id"] = media_id
    message["format"] = format
    message["recognition"] = recognition
    message = VoiceMessage(message)
    return message
