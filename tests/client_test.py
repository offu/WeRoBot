#!/usr/bin/env python
# -*- coding: utf-8 -*-

from werobot.client import BaseClient

auth_dict = {}

with open('auth.txt', 'r') as f:
    lines = list(f.readlines())
    auth_dict['email'] = lines[0]
    auth_dict['password'] = lines[1]


def test_client():
    print auth_dict
    pass
