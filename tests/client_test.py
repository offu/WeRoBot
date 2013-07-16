#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from werobot.client import WeixinClient


auth_dict = {}


with open('auth.txt', 'r') as f:
    lines = list(f.readlines())
    auth_dict['email'] = lines[0].strip()
    auth_dict['password'] = lines[1].strip()
    auth_dict['fakeid'] = lines[2].strip()


def test_client():
    print auth_dict
    c = WeixinClient(auth_dict['email'], auth_dict['password'])
    #c.push_text(auth_dict['fakeid'], 'sent by werobot')
    app_msgs = c.get_app_msgs()
    c.push_app(auth_dict['fakeid'], app_msgs[0]['appId'])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_client()
