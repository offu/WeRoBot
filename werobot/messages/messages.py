# -*- coding: utf-8 -*-

import six
from werobot.messages.entries import StringEntry, IntEntry, FloatEntry
from werobot.messages.base import WeRoBotMetaClass


class MessageMetaClass(WeRoBotMetaClass):
    pass


@six.add_metaclass(MessageMetaClass)
class WeChatMessage(object):
    message_id = IntEntry('MsgId', 0)
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
