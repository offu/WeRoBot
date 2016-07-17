# -*- coding: utf-8 -*-

import six
from werobot.messages.entries import *

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


@six.add_metaclass(MessageMetaClass)
class WeChatMessage(object):
    id = IntEntry('MsgId', 0)
    target = StringEntry('ToUserName')
    source = StringEntry('FromUserName')
    time = IntEntry('CreateTime', 0)

    def __init__(self, message):
        self.__dict__.update(message)


class TextMessage(WeChatMessage):
    __type__ = 'text'
    content = StringEntry('Content')


class ImageMessage(WeChatMessage):
    __type__ = 'image'
    img = StringEntry('PicUrl')


class LocationMessage(WeChatMessage):
    __type__ = 'location'
    location_x = FloatEntry('Location_X')
    location_y = FloatEntry('Location_Y')
    label = StringEntry('Label')
    scale = IntEntry('Scale')

    @property
    def location(self):
        return self.location_x, self.location_y


class LinkMessage(WeChatMessage):
    __type__ = 'link'
    title = StringEntry('Title')
    description = StringEntry('Description')
    url = StringEntry('Url')


class EventMessage(WeChatMessage):
    __type__ = ['event']

    def __init__(self, message):
        message.pop("type")
        self.type = message.pop('Event')
        self.type = str(self.type).lower()
        if self.type == "click":
            self.__class__.key = StringEntry('EventKey')
        elif self.type == "location":
            self.__class__.latitude = FloatEntry('Latitude')
            self.__class__.longitude = FloatEntry('Longitude')
            self.__class__.precision = FloatEntry('Precision')
        super(EventMessage, self).__init__(message)


class VoiceMessage(WeChatMessage):
    __type__ = 'voice'
    media_id = StringEntry('MediaId')
    format = StringEntry('Format')
    recognition = StringEntry('Recognition')


class VideoMessage(WeChatMessage):
    __type__ = ['video', 'shortvideo']
    media_id = StringEntry('MediaId')
    thumb_media_id = StringEntry('ThumbMediaId')


class UnknownMessage(WeChatMessage):
    __type__ = 'unknown'
