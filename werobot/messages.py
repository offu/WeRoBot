# -*- coding: utf-8 -*-


class WeChatMessage(object):
    def __init__(self, **kwargs):
        if 'msgid' in kwargs:
            self.id = int(kwargs['msgid'])
        if 'touser' in kwargs:
            self.target = kwargs['touser']
        if 'fromuser' in kwargs:
            self.source = kwargs['fromuser']
        if 'time' in kwargs:
            self.time = int(kwargs['time'])


class TextMessage(WeChatMessage):
    def __init__(self, content, **kwargs):
        super(TextMessage, self).__init__(**kwargs)

        self.type = 'text'
        self.content = content


class ImageMessage(WeChatMessage):
    def __init__(self, img, **kwargs):
        super(ImageMessage, self).__init__(**kwargs)
        self.type = 'image'
        self.img = img


class LocationMessage(WeChatMessage):
    def __init__(self, location_x, location_y, scale, label, **kwargs):
        super(LocationMessage, self).__init__(**kwargs)
        self.type = 'location'
        self.location = (float(location_x), float(location_y))
        self.scale = scale
        self.label = label


class LinkMessage(WeChatMessage):
    def __init__(self, title, description, url, **kwargs):
        super(LinkMessage, self).__init__(**kwargs)
        self.type = 'link'
        self.title = title
        self.description = description
        self.url = url


class EventMessage(WeChatMessage):
    def __init__(self, type, **kwargs):
        super(EventMessage, self).__init__(**kwargs)
        assert type in ['subscribe', 'unsubscribe', 'click']
        self.type = type
        if type == 'click':
            self.key = kwargs["eventkey"]


class UnknownMessage(WeChatMessage):
    def __init__(self, content):
        self.type = 'unknown'
        self.content = content
