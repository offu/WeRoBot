import requests


class ClientException(Exception):
    pass


def get_token(appid, appsecret):
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

