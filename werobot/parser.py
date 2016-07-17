# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import xmltodict
from werobot.messages import MESSAGE_TYPES, UnknownMessage
from werobot.messages import EVENT_TYPES, UnknownEvent


def parse_user_msg(xml):
    message = process_message(parse_xml(xml)) if xml else None
    return message


def parse_xml(text):
    xml_dict = xmltodict.parse(text)["xml"]
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
        message_type = EVENT_TYPES.get(message["type"], UnknownEvent)
    else:
        message_type = MESSAGE_TYPES.get(message["type"], UnknownMessage)
    return message_type(message)
