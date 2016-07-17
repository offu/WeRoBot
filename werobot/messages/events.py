# -*- coding: utf-8 -*-

import six
from werobot.messages.entries import *

EVENT_TYPES = {}


class EventMetaClass(type):
    def __new__(mcs, name, bases, attrs):
        return type.__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        if '__type__' in attrs:
            if isinstance(attrs['__type__'], list):
                for _type in attrs['__type__']:
                    EVENT_TYPES[_type] = cls
            else:
                EVENT_TYPES[attrs['__type__']] = cls
        type.__init__(cls, name, bases, attrs)


@six.add_metaclass(EventMetaClass)
class WeChatEvent(object):
    target = StringEntry('ToUserName')
    source = StringEntry('FromUserName')
    time = IntEntry('CreateTime')

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


class UnknownEvent(WeChatEvent):
    __type__ = 'unknown_event'
