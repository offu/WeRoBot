from xml.etree import ElementTree
from tornado.util import ObjectDict
from .messages import TextMessage, ImageMessage, LocationMessage

MSG_TYPE_TEXT = 'text'
MSG_TYPE_LOCATION = 'location'
MSG_TYPE_IMAGE = 'image'


def decode(s):
    if isinstance(s, str):
        return s.decode('utf-8')
    return s


def parse_user_msg(xml):
    if not xml:
        return None
    parser = ElementTree.fromstring(xml)
    msg_type = decode(parser.find('MsgType').text)
    touser = decode(parser.find('ToUserName').text)
    fromuser = decode(parser.find('FromUserName').text)
    create_at = int(parser.find('CreateTime').text)
    msg = ObjectDict(
        touser=touser,
        fromuser=fromuser,
        time=create_at
    )
    if msg_type == MSG_TYPE_TEXT:
        msg.content = decode(parser.find('Content').text)
        return TextMessage(**msg)
    elif msg_type == MSG_TYPE_LOCATION:
        msg.location_x = decode(parser.find('Location_X').text)
        msg.location_y = decode(parser.find('Location_Y').text)
        msg.scale = int(parser.find('Scale').text)
        msg.label = decode(parser.find('Label').text)
        return LocationMessage(**msg)
    elif msg_type == MSG_TYPE_IMAGE:
        msg.img = decode(parser.find('PicUrl').text)
        return ImageMessage(**msg)
