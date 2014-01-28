from xml.etree import ElementTree

from werobot.messages import MESSAGE_TYPES, UnknownMessage
from werobot.utils import to_text


def parse_user_msg(xml):
    """
    Parse xml from wechat server and return an Message
    :param xml: raw xml from wechat server.
    :return: an Message object
    """
    if not xml:
        return

    wechat_message = dict((child.tag, to_text(child.text))
                          for child in ElementTree.fromstring(xml))
    wechat_message["raw"] = xml
    wechat_message["type"] = wechat_message.pop("MsgType").lower()

    message_type = MESSAGE_TYPES.get(wechat_message["type"], UnknownMessage)
    return message_type(wechat_message)
