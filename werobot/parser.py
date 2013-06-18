# -*- coding: utf-8 -*-

from xml.etree import ElementTree

from .messages import *
from .messages import UnknownMessage
from .utils import to_unicode


def parse_user_msg(xml):
    """
    Parse xml from wechat server and return an Message
    :param xml: raw xml from wechat server.
    :return: an Message object
    """
    if not xml:
        return

    _msg = dict((child.tag, to_unicode(child.text))
                for child in ElementTree.fromstring(xml))

    msg_type = _msg.get('MsgType')
    touser = _msg.get('ToUserName')
    fromuser = _msg.get('FromUserName')
    create_at = int(_msg.get('CreateTime'))
    msg = dict(
        touser=touser,
        fromuser=fromuser,
        time=create_at
    )
    if msg_type == 'text':
        msg["content"] = _msg.get('Content')
        return TextMessage(**msg)
    elif msg_type == 'location':
        msg["location_x"] = _msg.get('Location_X')
        msg["location_y"] = _msg.get('Location_Y')
        msg["scale"] = int(_msg.get('Scale'))
        msg["label"] = _msg.get('Label')
        return LocationMessage(**msg)
    elif msg_type == 'image':
        msg["img"] = _msg.get('PicUrl')
        return ImageMessage(**msg)
    elif msg_type == 'event':
        msg["type"] = _msg.get('Event').lower()
        if msg["type"] == "location":
            msg["latitude"] = _msg.get('Latitude')
            msg["longitude"] = _msg.get('Longitude')
            msg["precision"] = _msg.get('Precision')
        return EventMessage(**msg)
    elif msg_type == 'link':
        return LinkMessage(**msg)
    else:
        return UnknownMessage(xml)
