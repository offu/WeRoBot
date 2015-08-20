# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import xmltodict

from werobot.messages import MESSAGE_TYPES, UnknownMessage


def parse_user_msg(xml):
    return process_message(parse_xml(xml))


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
    message_type = MESSAGE_TYPES.get(message["type"], UnknownMessage)
    return message_type(message)
