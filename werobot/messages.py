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
    def __init__(self, entry, type, default=None):
        self.entry = entry
        self.default = default
        self.type = type

    def __get__(self, instance, owner):
        result = {
            0: lambda v: int(v),
            1: lambda v: float(v),
            2: lambda v: str(v),
        }
        return result[self.type](instance.__dict__.get(self.entry, self.default))


class TupleEntry(object):
    def __init__(self, entry, type):
        self.entry1 = entry[0]
        self.entry2 = entry[1]
        self.type = type

    def __get__(self, instance, owner):
        result = {
            3: lambda v: float(v),
        }
        return result[self.type](instance.__dict__.get(self.entry1)), result[self.type](
            instance.__dict__.get(self.entry2))


class EntryGenerator(object):
    Int = 0
    Float = 1
    String = 2
    FloatTuple = 3

    def generate(self, entry, _type, default=None):
        if _type in (0, 2):
            e = BaseEntry(entry, _type, default)
            return e
        if _type == 3:
            e = TupleEntry(entry, _type)
            return e


generator = EntryGenerator()


@six.add_metaclass(MessageMetaClass)
class WeChatMessage(object):
    id = generator.generate('MsgId', EntryGenerator.Int, 0)
    target = generator.generate('ToUserName', EntryGenerator.String)
    source = generator.generate('FromUserName', EntryGenerator.String)
    time = generator.generate('CreateTime', EntryGenerator.Int, 0)

    def __init__(self, message):
        self.__dict__.update(message)


class TextMessage(WeChatMessage):
    __type__ = 'text'
    content = generator.generate('Content', EntryGenerator.String)


class ImageMessage(WeChatMessage):
    __type__ = 'image'
    img = generator.generate('PicUrl', EntryGenerator.String)


class LocationMessage(WeChatMessage):
    __type__ = 'location'
    location_x = generator.generate('Location_X', EntryGenerator.Float)
    location_y = generator.generate('Location_Y', EntryGenerator.Float)
    label = generator.generate('Label', EntryGenerator.String)
    scale = generator.generate('Scale', EntryGenerator.Int)
    location = generator.generate(('Location_X', 'Location_Y'), EntryGenerator.FloatTuple)


class LinkMessage(WeChatMessage):
    __type__ = 'link'
    title = generator.generate('Title', EntryGenerator.String)
    description = generator.generate('Description', EntryGenerator.String)
    url = generator.generate('Url', EntryGenerator.String)


class EventMessage(WeChatMessage):
    __type__ = ['event']

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
    media_id = generator.generate('MediaId', generator.String)
    format = generator.generate('Format', generator.String)
    recognition = generator.generate('Recognition', generator.String)


class VideoMessage(WeChatMessage):
    __type__ = ['video', 'shortvideo']
    media_id = generator.generate('MediaId', generator.String)
    thumb_media_id = generator.generate('ThumbMediaId', generator.String)


class UnknownMessage(WeChatMessage):
    def __init__(self, message):
        self.type = 'unknown'
        super(UnknownMessage, self).__init__(message)
