# -*- coding: utf-8 -*-

import requests


class ClientException(Exception):
    pass


def get_token(appid, appsecret):
    """
    获取 Access Token 。
    详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=通用接口文档

    :param appid: 第三方用户唯一凭证
    :param appsecret: 第三方用户唯一凭证密钥，即 App Secret
    """
    r = requests.get(
        "https://api.weixin.qq.com/cgi-bin/token",
        params={
            "grant_type": "client_credential",
            "appid": appid,
            "secret": appsecret
        }
    )
    r.raise_for_status()
    json = r.json()
    if "access_token" in json:
        return json["access_token"]
    raise ClientException(json["errmsg"])

