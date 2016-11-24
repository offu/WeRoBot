# -*- coding: utf-8 -*-

import six
from werobot.messages.entries import StringEntry, IntEntry, FloatEntry
from werobot.messages.base import WeRoBotMetaClass


class EventMetaClass(WeRoBotMetaClass):
    pass


@six.add_metaclass(EventMetaClass)
class WeChatEvent(object):
    target = StringEntry('ToUserName')
    source = StringEntry('FromUserName')
    time = IntEntry('CreateTime')
    message_id = IntEntry('MsgID', 0)

    def __init__(self, message):
        self.__dict__.update(message)


class TicketEvent(WeChatEvent):
    key = StringEntry('EventKey')
    ticket = StringEntry('Ticket')


class SubscribeEvent(TicketEvent):
    __type__ = 'subscribe_event'


class UnSubscribeEvent(WeChatEvent):
    __type__ = 'unsubscribe_event'


class ScanEvent(TicketEvent):
    __type__ = 'scan_event'


class SimpleEvent(WeChatEvent):
    key = StringEntry('EventKey')


class ClickEvent(SimpleEvent):
    __type__ = 'click_event'


class ViewEvent(SimpleEvent):
    __type__ = 'view_event'


class LocationEvent(WeChatEvent):
    __type__ = 'location_event'
    latitude = FloatEntry('Latitude')
    longitude = FloatEntry('Longitude')
    precision = FloatEntry('Precision')


class TemplateSendJobFinishEvent(WeChatEvent):
    __type__ = 'templatesendjobfinish_event'
    status = StringEntry('Status')


class UnknownEvent(WeChatEvent):
    __type__ = 'unknown_event'
