# -*- coding: utf-8 -*-

import imp
import time

class ConfigAttribute(object):
    """
    让一个属性指向一个配置
    """

    def __init__(self, name, appid, appsecret):
        self.__name__ = name
        self._token=None
        self.appid = appid
        self.appsecret=appsecret
        self.token_expires_at = None


    def __get__(self, obj, type=None):
        if obj is None:
            return self
        rv = obj.config[self.__name__]
        return rv

    def __set__(self, obj, value):
        obj.config[self.__name__] = value


class Config(dict):
    def from_pyfile(self, filename):
        """
        在一个 Python 文件中读取配置。

        :param filename: 配置文件的文件名。
        """
        d = imp.new_module('config')
        d.__file__ = filename
        with open(filename) as config_file:
            exec (compile(config_file.read(), filename, 'exec'), d.__dict__)
        self.from_object(d)
        return True

    def from_object(self, obj):
        """
        在给定的 Python 对象中读取配置。

        :param obj: 一个 Python 对象
        """
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def refresh_access_token(self):
        """
        获取 Access Token 。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=通用接口文档

        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://api.weixin.qq.com/cgi-bin/token",
            params={
                "grant_type": "client_credential",
                "appid": self.appid,
                "secret": self.appsecret
            }
        )

    def get_access_token(self):
        """
        判断现有的token是否过期。
        用户需要多进程或者多机部署可以手动重写这个函数
        来自定义token的存储，刷新策略。
        :return:
        """
        if self._token:
            now = time.time()
            if self.token_expires_at - now > 60:
                return self._token
        json = self.refresh_access_token()
        self._token = json["access_token"]
        self.token_expires_at = int(time.time()) + json["expires_in"]
        return self._token

    @property
    def access_token(self):
        return self.get_access_token()