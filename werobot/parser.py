# -*- coding: utf-8 -*-

import re
import xmltodict
from werobot.messages.messages import MessageMetaClass, UnknownMessage
from werobot.messages.events import EventMetaClass, UnknownEvent


def parse_user_msg(xml):
    message = process_message(parse_xml(xml)) if xml else None
    return message


def parse_xml(text):
    text_clean = re.sub(b'[\x00-\x09\x0B-\x0C\x0E-\x1F]', b'', text)
    xml_dict = xmltodict.parse(text_clean)["xml"]
    xml_dict["raw"] = text
    return xml_dict


def process_message(message):
    """
    Process a message dict and return a Message Object
    :param message: Message dict returned by `parse_xml` function
    :return: Message Object
    """
    message["type"] = message.pop("MsgType").lower()
    if message["type"] == 'event':
        message["type"] = str(message.pop("Event")).lower() + '_event'
        message_type = EventMetaClass.TYPES.get(message["type"], UnknownEvent)
    else:
        message_type = MessageMetaClass.TYPES.get(
            message["type"], UnknownMessage
        )
    return message_type(message)
