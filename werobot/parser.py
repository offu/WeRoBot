from xml.etree import ElementTree

from .messages import TextMessage, LocationMessage, ImageMessage, EventMessage
from .messages import LinkMessage, VoiceMessage, UnknownMessage
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
        if msg["type"] == "click":
            msg["eventkey"] = _msg.get('EventKey')
        return EventMessage(**msg)
    elif msg_type == 'link':
        msg["title"] = _msg.get('Title')
        msg["description"] = _msg.get('Description')
        msg["url"] = _msg.get('Url')
        return LinkMessage(**msg)
    elif msg_type == 'voice':
        msg["media_id"] = _msg.get('MediaId')
        msg["format"] = _msg.get('Format')
        msg["recognition"] = _msg.get('Recognition')
        return VoiceMessage(**msg)
    else:
        return UnknownMessage(xml)
