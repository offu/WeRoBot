# -*- coding: utf-8 -*-

import time
import requests


class ClientException(Exception):
    pass


def check_error(json):
    """
    检测微信公众平台返回值中是否包含错误的返回码。
    如果返回码提示有错误，抛出一个 :class:`ClientException` 异常。否则返回 True 。
    """
    if "errcode" in json and json["errcode"] != 0:
        raise ClientException("{}: {}".format(json["errcode"], json["errmsg"]))
    return json


class Client(object):
    def __init__(self, appid, appsecret):
        self.appid = appid
        self.appsecret = appsecret
        self._token = None
        self.token_expires_at = None

    def _request(self, method, url, **kwargs):
        r = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        r.raise_for_status()
        json = r.json()
        if check_error(json):
            return json

    def grant_token(self):
        """
        获取 Access Token 。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=通用接口文档

        :param appid: 第三方用户唯一凭证
        :param appsecret: 第三方用户唯一凭证密钥，即 App Secret

        :return: 返回的 JSON 数据包
        """
        return self._request(
            method="get",
            url="https://api.weixin.qq.com/cgi-bin/token",
            params={
                "grant_type": "client_credential",
                "appid": self.appid,
                "secret": self.appsecret
            }
        )


    @property
    def token(self):
        if self._token:
            now = time.time()
            if self.token_expires_at - now > 60:
                return self._token
        json = self.grant_token()
        self._token = json["access_token"]
        self.token_expires_at = int(time.time()) + json["expires_in"]
        return self._token

    def create_menu(self, menu_data):
        """
        创建自定义菜单。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单创建接口

        :param access_token: Access Token，可以使用 :func:`get_token` 获取。
        :param menu_data: Python 字典。

        :return: 返回的 JSON 数据包
        """
        return self._request(
            method="post",
            url="https://api.weixin.qq.com/cgi-bin/menu/create",
            params={
                "access_token": self.token,
            },
            data=menu_data
        )

    def get_menu(self):
        """
        查询自定义菜单。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单查询接口

        :return: 返回的 JSON 数据包
        """
        return self._request(
            method="get",
            url="https://api.weixin.qq.com/cgi-bin/menu/get",
            params={
                "access_token": self.token,
            }
        )

    def delete_menu(self):
        """
        删除自定义菜单。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=自定义菜单删除接口

        :return: 返回的 JSON 数据包
        """
        return self._request(
            method="get",
            url="https://api.weixin.qq.com/cgi-bin/menu/delete",
            params={
                "access_token": self.token,
            }
        )

    def upload_media(self, type, media):
        """
        上传多媒体文件。
        详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=上传下载多媒体文件

        :param access_token: Access Token，可以使用 :func:`get_token` 获取。
        :param type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        :param media:要上传的文件，一个 File-object

        :return: 返回的 JSON 数据包
        """
        return self._request(
            method="post",
            url="https://api.weixin.qq.com/cgi-bin/menu/create",
            params={
                "access_token": self.token,
                "type": type
            },
            files={
                "media": media
            }
        )
