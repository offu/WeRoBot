# -*- coding: utf-8 -*-

import requests


class ClientException(Exception):
    pass


def check_error(json):
    """
    检测微信公众平台返回值中是否包含错误的返回码。
    如果返回码提示有错误，抛出一个 :class:`ClientException` 异常。否则返回 True 。
    """
    if "errcode" in json and json["errcode"] != 0:
        raise ClientException(json["errmsg"])
    return True


def get_token(appid, appsecret):
    """
    获取 Access Token 。
    详情请参考 http://mp.weixin.qq.com/wiki/index.php?title=通用接口文档

    :param appid: 第三方用户唯一凭证
    :param appsecret: 第三方用户唯一凭证密钥，即 App Secret
    :return: Access Token 值
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
    return check_error(json)


def create_menu(access_token, menu_data):
    """
    创建自定义菜单。

    :param access_token: Access Token，可以使用 :func:`get_token` 获取。
    :param menu_data:
    """
    r = requests.get(
        url="https://api.weixin.qq.com/cgi-bin/menu/create",
        params={
            "access_token": "access_token",
        },
        data=menu_data
    )
    r.raise_for_status()
    json = r.json()
    if json.get("errcode", 0) == 0:
        return True
    raise ClientException(json["errmsg"])
