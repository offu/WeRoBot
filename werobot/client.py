# -*- coding: utf-8 -*-
#
# Originally modified from Vincent Ting's code

import time
import hashlib
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


class LoginError(Exception):
    pass


class RequestError(Exception):
    def __init__(self, resp):
        self.resp = resp

    def __str__(self):
        return 'RequestError resp: code=%s, content=%s' %\
               self.resp.status_code, self.resp.content


class WeixinClient(object):
    LOGIN_URL = 'http://mp.weixin.qq.com/cgi-bin/login?lang=en_US'

    PUSH_URL = 'http://mp.weixin.qq.com/cgi-bin/singlesend?t=ajax-response&lang=zh_CN'

    APP_MSG_URL = 'http://mp.weixin.qq.com/cgi-bin/operate_appmsg?token={0}&lang=zh_CN&sub=list&t=ajax-appmsgs-fileselect&type=10&pageIdx=0&pagesize=10&formid=file_from_{1}000&subtype=3'

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.password_hash = hashlib.md5(self.password[0:16]).hexdigest()

        self.login()

    def login(self):
        body_data = {
            'username': self.email,
            'pwd': self.password_hash,
            'imgcode': '',
            'f': 'json'
        }

        resp = self.post(self.LOGIN_URL, data=body_data)
        resp_data = resp.json()

        if resp_data['ErrCode'] not in (0, 65202):
            raise LoginError('Failed to login, response: %s' % resp.content)

        self.token = resp_data['ErrMsg'].split('=')[-1]
        logging.debug('get token: %s', self.token)

        self.cookies = dict(resp.cookies)

    def _request(self, method, *args, **kwargs):
        headers = _FAKE_HEADERS.copy()
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers

        if hasattr(self, 'cookies'):
            kwargs['cookies'] = self.cookies

        # logging.debug('request kwargs: %s', kwargs)
        func = getattr(requests, method)
        resp = func(*args, **kwargs)
        logging.debug('resp: code=%s, content=%s', resp.status_code, resp.content)
        logging.debug('request headers: %s', resp.request.headers)

        if resp.status_code != 200:
            raise RequestError(resp)
        try:
            resp_data = resp.json()
        except Exception:
            # TODO use json decode exception
            pass
        else:
            if resp_data.get('ret') == "-20000" or\
               resp_data.get('Ret') == "-20000":
                raise RequestError(resp)
        return resp

    def get(self, *args, **kwargs):
        return self._request('get', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._request('post', *args, **kwargs)

    def _push(self, fakeid, extra_data):
        extra_headers = {
            'Referer': 'http://mp.weixin.qq.com/cgi-bin/singlemsgpage?fromfakeid=%s'
                       '&msgid=&source=&count=20&t=wxm-singlechat&lang=zh_CN' % fakeid
        }
        data = {
            'error': 'false',
            'token': str(self.token),
            'tofakeid': fakeid,
            'ajax': 1
        }
        data.update(extra_data)

        resp = self.post(self.PUSH_URL, data=data, headers=extra_headers)

        return resp.json()

    def push_text(self, fakeid, text):
        return self._push(fakeid, {
            'type': 1,
            'content': text
        })

    def push_app(self, fakeid, app_msg_id):
        return self._push(fakeid, {
            'type': 10,
            'fid': app_msg_id,
            'appmsgid': app_msg_id
        })

    def get_app_msgs(self):
        resp = self.post(
            self.APP_MSG_URL.format(self.token, int(time.time())),
            data={
                'token': self.token,
                'ajax': 1
            })
        resp_data = resp.json()
        return resp_data['List']


class ClientLoginException(Exception):
    pass
