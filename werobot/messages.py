# -*- coding: utf-8 -*-

MESSAGE_TYPES = {}


def handle_for_type(type):
    def register(f):
        MESSAGE_TYPES[type] = f
        return f
    return register


class WeChatMessage(object):
    def __init__(self, message):
        self.id = int(message.pop("MsgId", 0))
        self.target = message.pop("ToUserName", None)
        self.source = message.pop('FromUserName', None)
        self.time = int(message.get('CreateTime', 0))
        self.__dict__.update(message)


@handle_for_type("text")
class TextMessage(WeChatMessage):
    def __init__(self, message):
        self.content = message.pop("Content")
        super(TextMessage, self).__init__(message)


@handle_for_type("image")
class ImageMessage(WeChatMessage):
    def __init__(self, message):
        self.img = message.pop("PicUrl")
        super(ImageMessage, self).__init__(message)


@handle_for_type("location")
class LocationMessage(WeChatMessage):
    def __init__(self, message):
        location_x = message.pop('Location_X')
        location_y = message.pop('Location_Y')
        self.location = (float(location_x), float(location_y))
        self.scale = int(message.pop('Scale'))
        self.label = message.pop('Label')
        super(LocationMessage, self).__init__(message)


@handle_for_type("link")
class LinkMessage(WeChatMessage):
    def __init__(self, message):
        self.title = message.pop('Title')
        self.description = message.pop('Description')
        self.url = message.pop('Url')
        super(LinkMessage, self).__init__(message)


@handle_for_type("event")
class EventMessage(WeChatMessage):
    def __init__(self, message):
        message.pop("type")
        self.type = message.pop("Event").lower()
        if self.type == "click":
            self.key = message.pop('EventKey')
        elif self.type == "location":
            self.latitude = float(message.pop("Latitude"))
            self.longitude = float(message.pop("Longitude"))
            self.precision = float(message.pop("Precision"))
        super(EventMessage, self).__init__(message)


@handle_for_type("voice")
class VoiceMessage(WeChatMessage):
    def __init__(self, message):
        self.media_id = message.pop('MediaId')
        self.format = message.pop('Format')
        self.recognition = message.pop('Recognition')
        super(VoiceMessage, self).__init__(message)


class UnknownMessage(WeChatMessage):
    def __init__(self, message):
        self.type = 'unknown'
        super(UnknownMessage, self).__init__(message)
