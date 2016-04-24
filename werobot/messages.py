# -*- coding: utf-8 -*-

import six

MESSAGE_TYPES = {}


class MessageMetaClass(type):
    def __new__(mcs, name, bases, attrs):
        for k, v in attrs.items():
            if isinstance(v, MessageEntry):
                pass
        return type.__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        if '__type__' in attrs.keys():
            if isinstance(attrs['__type__'], list):
                for _type in attrs['__type__']:
                    MESSAGE_TYPES[_type] = cls
            else:
                MESSAGE_TYPES[attrs['__type__']] = cls
        type.__init__(cls, name, bases, attrs)


class MessageEntry(object):
    def __init__(self, entry, default=None):
        self.entry = entry
        self.default = default

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.entry, self.default)


class IntMessageEntry(MessageEntry):
    def __get__(self, instance, owner):
        value = instance.__dict__.get(self.entry, self.default)
        if value:
            return int(value)
        else:
            return None


class FloatMessageEntry(MessageEntry):
    def __get__(self, instance, owner):
        value = instance.__dict__.get(self.entry, self.default)
        if value:
            return float(value)
        else:
            return None


class TupleMessageEntry(object):
    def __init__(self, t1, t2, default=None):
        self.t1 = t1;
        self.t2 = t2;
        self.default = default

    def __get__(self, instance, owner):
        v1 = instance.__dict__.get(self.t1, None)
        v2 = instance.__dict__.get(self.t2, None)
        if v1 or v2:
            return (v1, v2)
        else:
            return self.default


class FloatTupleMessageEntry(TupleMessageEntry):
    def __get__(self, instance, owner):
        v1 = instance.__dict__.get(self.t1, None)
        v2 = instance.__dict__.get(self.t2, None)
        if v1 or v2:
            return (float(v1), float(v2))
        else:
            return self.default


@six.add_metaclass(MessageMetaClass)
class WeChatMessage(object):
    id = IntMessageEntry('MsgId', 0)
    target = MessageEntry('ToUserName')
    source = MessageEntry('FromUserName')
    target = MessageEntry('ToUserName')
    time = IntMessageEntry('CreateTime', 0)

    def __init__(self, message):
        self.__dict__.update(message)


class TextMessage(WeChatMessage):
    __type__ = 'text'
    content = MessageEntry('Content')


class ImageMessage(WeChatMessage):
    __type__ = 'image'
    img = MessageEntry('PicUrl')


class LocationMessage(WeChatMessage):
    __type__ = 'location'
    location_x = FloatMessageEntry('Location_X')
    location_y = FloatMessageEntry('Location_Y')
    label = MessageEntry('Label')
    scale = IntMessageEntry('Scale')
    location = FloatTupleMessageEntry('Location_X', 'Location_Y')


class LinkMessage(WeChatMessage):
    __type__ = 'link'
    title = MessageEntry('Title')
    description = MessageEntry('Description')
    url = MessageEntry('Url')


class EventMessage(WeChatMessage):
    __type__ = 'event'

    def __init__(self, message):
        message.pop("type")
        self.type = message.pop('Event')
        self.type = str(self.type).lower()
        if self.type == "click":
            self.key = message.pop('EventKey')
        elif self.type == "location":
            self.latitude = float(message.pop("Latitude"))
            self.longitude = float(message.pop("Longitude"))
            self.precision = float(message.pop("Precision"))
        super(EventMessage, self).__init__(message)


class VoiceMessage(WeChatMessage):
    __type__ = 'voice'
    media_id = MessageEntry('MediaId')
    format = MessageEntry('Format')
    recognition = MessageEntry('Recognition')


class VideoMessage(WeChatMessage):
    __type__ = ['video', 'shortvideo']
    media_id = MessageEntry('MediaId')
    thumb_media_id = MessageEntry('ThumbMediaId')


class UnknownMessage(WeChatMessage):
    def __init__(self, message):
        self.type = 'unknown'
        super(UnknownMessage, self).__init__(message)
