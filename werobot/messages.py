# -*- coding: utf-8 -*-

import six

MESSAGE_TYPES = {}


class MessageMetaClass(type):
    def __new__(mcs, name, bases, attrs):
        return type.__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        if '__type__' in attrs:
            if isinstance(attrs['__type__'], list):
                for _type in attrs['__type__']:
                    MESSAGE_TYPES[_type] = cls
            else:
                MESSAGE_TYPES[attrs['__type__']] = cls
        type.__init__(cls, name, bases, attrs)


class BaseEntry(object):
    INT = 0
    FLOAT = 1
    STRING = 2

    def __init__(self, entry, type, default=None):
        self.entry = entry
        self.default = default
        self.type = type

    def __get__(self, instance, owner):
        result = {
            self.INT: lambda v: int(v),
            self.FLOAT: lambda v: float(v),
            self.STRING: lambda v: v,
        }
        return result[self.type](instance.__dict__.get(self.entry, self.default))


class TupleEntry(object):
    FLOAT = 3

    def __init__(self, entry, type):
        self.entry1 = entry[0]
        self.entry2 = entry[1]
        self.type = type

    def __get__(self, instance, owner):
        result = {
            self.FLOAT: lambda v: float(v),
        }
        return result[self.type](instance.__dict__.get(self.entry1)), result[self.type](
            instance.__dict__.get(self.entry2))


@six.add_metaclass(MessageMetaClass)
class WeChatMessage(object):
    id = BaseEntry('MsgId', BaseEntry.INT, 0)
    target = BaseEntry('ToUserName', BaseEntry.STRING)
    source = BaseEntry('FromUserName', BaseEntry.STRING)
    time = BaseEntry('CreateTime', BaseEntry.INT, 0)

    def __init__(self, message):
        self.__dict__.update(message)


class TextMessage(WeChatMessage):
    __type__ = 'text'
    content = BaseEntry('Content', BaseEntry.STRING)


class ImageMessage(WeChatMessage):
    __type__ = 'image'
    img = BaseEntry('PicUrl', BaseEntry.STRING)


class LocationMessage(WeChatMessage):
    __type__ = 'location'
    location_x = BaseEntry('Location_X', BaseEntry.FLOAT)
    location_y = BaseEntry('Location_Y', BaseEntry.FLOAT)
    label = BaseEntry('Label', BaseEntry.STRING)
    scale = BaseEntry('Scale', BaseEntry.INT)
    location = TupleEntry(['Location_X', 'Location_Y'], TupleEntry.FLOAT)


class LinkMessage(WeChatMessage):
    __type__ = 'link'
    title = BaseEntry('Title', BaseEntry.STRING)
    description = BaseEntry('Description', BaseEntry.STRING)
    url = BaseEntry('Url', BaseEntry.STRING)


class EventMessage(WeChatMessage):
    __type__ = ['event']

    def __init__(self, message):
        message.pop("type")
        self.type = message.pop('Event')
        self.type = str(self.type).lower()
        if self.type == "click":
            self.__class__.key = BaseEntry('EventKey', BaseEntry.STRING)
        elif self.type == "location":
            self.__class__.latitude = BaseEntry('Latitude', BaseEntry.FLOAT)
            self.__class__.longitude = BaseEntry('Longitude', BaseEntry.FLOAT)
            self.__class__.precision = BaseEntry('Precision', BaseEntry.FLOAT)
        super(EventMessage, self).__init__(message)


class VoiceMessage(WeChatMessage):
    __type__ = 'voice'
    media_id = BaseEntry('MediaId', BaseEntry.STRING)
    format = BaseEntry('Format', BaseEntry.STRING)
    recognition = BaseEntry('Recognition', BaseEntry.STRING)


class VideoMessage(WeChatMessage):
    __type__ = ['video', 'shortvideo']
    media_id = BaseEntry('MediaId', BaseEntry.STRING)
    thumb_media_id = BaseEntry('ThumbMediaId', BaseEntry.STRING)


class UnknownMessage(WeChatMessage):
    __type__ = 'unknown'
