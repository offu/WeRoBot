# -*- coding: utf-8 -*-
#
# Originally modified from Vincent Ting's code

import cookielib
import urllib2
import urllib
import json
import poster
import hashlib
import time
import re

import requests
import logging


_FAKE_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'mp.weixin.qq.com',
    'Origin': 'mp.weixin.qq.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22'
}


class BaseClient(object):
    LOGIN_URL = 'http://mp.weixin.qq.com/cgi-bin/login?lang=en_US'

    def __init__(self, email, password):
        """
        登录公共平台服务器，如果失败将报客户端登录异常错误
        :param email:
        :param password:
        :raise:
        """
        data = {
            'username': email,
            'pwd': hashlib.md5(password[0:16]).hexdigest(),
            'imgcode': '',
            'f': 'json'
        }
        resp = self.post(self.LOGIN_URL, data=data)
        logging.debug('resp: code=%s, content=%s', resp.code, resp.content)

    def _request(self, method, *args, **kwargs):
        if 'headers' in kwargs:
            headers = kwargs['headers']
            headers.update(_FAKE_HEADERS)
        else:
            headers = _FAKE_HEADERS.copy()
        kwargs['headers'] = headers

        func = getattr(requests, method)
        return func(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self._request('get', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._request('post', *args, **kwargs)


class ClientLoginException(Exception):
    pass
