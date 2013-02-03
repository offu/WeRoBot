from xml.etree import ElementTree

from .messages import TextMessage, ImageMessage, LocationMessage, UnknownMessage
from .utils import to_unicode

MSG_TYPE_TEXT = 'text'
MSG_TYPE_LOCATION = 'location'
MSG_TYPE_IMAGE = 'image'


def parse_user_msg(xml):
    if not xml:
        return None
    parser = ElementTree.fromstring(xml)
    msg_type = to_unicode(parser.find('MsgType').text)
    touser = to_unicode(parser.find('ToUserName').text)
    fromuser = to_unicode(parser.find('FromUserName').text)
    create_at = int(parser.find('CreateTime').text)
    msg = dict(
        touser=touser,
        fromuser=fromuser,
        time=create_at
    )
    if msg_type == MSG_TYPE_TEXT:
        msg["content"] = to_unicode(parser.find('Content').text)
        return TextMessage(**msg)
    elif msg_type == MSG_TYPE_LOCATION:
        msg["location_x"] = to_unicode(parser.find('Location_X').text)
        msg["location_y"] = to_unicode(parser.find('Location_Y').text)
        msg["scale"] = int(parser.find('Scale').text)
        msg["label"] = to_unicode(parser.find('Label').text)
        return LocationMessage(**msg)
    elif msg_type == MSG_TYPE_IMAGE:
        msg["img"] = to_unicode(parser.find('PicUrl').text)
        return ImageMessage(**msg)
    else:
        return UnknownMessage(xml)
