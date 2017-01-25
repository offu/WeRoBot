# -*- coding: utf-8 -*-
import os
import responses
import json

from werobot import WeRoBot
from werobot.config import Config
from werobot.client import Client, check_error, ClientException

basedir = os.path.dirname(os.path.abspath(__file__))

TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
json_header = {'content-type': 'application/json'}
menu_data = {
    "button": [
        {
            "type": "click",
            "name": "今日歌曲",
            "key": "V1001_TODAY_MUSIC"
        },
        {
            "type": "click",
            "name": "歌手简介",
            "key": "V1001_TODAY_SINGER"
        },
        {
            "name": "菜单",
            "sub_button": [
                {
                    "type": "view",
                    "name": "搜索",
                    "url": "http://www.soso.com/"
                },
                {
                    "type": "view",
                    "name": "视频",
                    "url": "http://v.qq.com/"
                },
                {
                    "type": "click",
                    "name": "赞一下我们",
                    "key": "V1001_GOOD"
                }
            ]
        }
    ]}


# callbacks
def token_callback(request):
    return 200, json_header, json.dumps({"access_token": "ACCESS_TOKEN", "expires_in": 7200})


def check_menu_data(item):
    keys = item.keys()
    assert "name" in keys
    if "sub_button" in keys:
        for button in item["sub_button"]:
            check_menu_data(button)
        return
    assert "type" in keys
    if "type" == "click":
        assert "key" in keys
    elif "type" == "view":
        assert "url" in keys
    elif "type" == "media_id" or "type" == "view_limited":
        assert "media_id" in keys


# test case
def test_id_and_secret():
    config = Config()
    config.from_pyfile(os.path.join(basedir, "client_config.py"))
    client = Client(config)
    assert client.appid == "123"
    assert client.appsecret == "321"


def test_robot_client():
    robot = WeRoBot()
    assert robot.client.config == robot.config


def test_check_error():
    error_json = dict(
        error_code=0
    )
    assert error_json == check_error(error_json)

    error_json["error_code"] = 1
    error_json["error_message"] = "test"
    try:
        check_error(error_json)
    except ClientException as e:
        assert str(e) == "1: test"


@responses.activate
def test_grant_token():
    responses.add_callback(responses.GET, TOKEN_URL, callback=token_callback)
    config = Config()
    config.from_pyfile(os.path.join(basedir, "client_config.py"))
    client = Client(config)

    client.grant_token()
    assert client.token == "ACCESS_TOKEN"


@responses.activate
def test_client_request():
    EMPTY_PARAMS_URL = "http://empty-params.werobot.com/"
    DATA_EXISTS_URL = "http://data-exists.werobot.com/"

    def empty_params_callback(request):
        assert request.url[request.url.rfind("=") + 1:] == client.token
        return 200, json_header, json.dumps({"test": "test"})

    def data_exists_url(request):
        assert json.loads(request.body.decode('utf-8')) == {"test": "test"}
        return 200, json_header, json.dumps({"test": "test"})

    responses.add_callback(responses.POST, DATA_EXISTS_URL, callback=data_exists_url)
    responses.add_callback(responses.GET, EMPTY_PARAMS_URL, callback=empty_params_callback)
    responses.add_callback(responses.GET, TOKEN_URL, callback=token_callback)

    config = Config()
    config.from_pyfile(os.path.join(basedir, "client_config.py"))
    client = Client(config)

    r = client.get(url=EMPTY_PARAMS_URL)
    assert r == {"test": "test"}

    r = client.post(url=DATA_EXISTS_URL, data={"test": "test"})
    assert r == {"test": "test"}


@responses.activate
def test_client_create_menu():
    CREATE_URL = "https://api.weixin.qq.com/cgi-bin/menu/create"
    responses.add_callback(responses.GET, TOKEN_URL, callback=token_callback)
    config = Config()
    config.from_pyfile(os.path.join(basedir, "client_config.py"))
    client = Client(config)

    def create_menu_callback(request):
        try:
            body = json.loads(request.body.decode("utf-8"))["button"]
        except KeyError:
            return 200, json_header, json.dumps({"errcode": 1, "errmsg": "error"})
        try:
            for item in body:
                check_menu_data(item)
        except AssertionError:
            return 200, json_header, json.dumps({"errcode": 1, "errmsg": "error"})
        return 200, json_header, json.dumps({"errcode": 0, "errmsg": "ok"})

    responses.add_callback(responses.POST, CREATE_URL, callback=create_menu_callback)

    r = client.create_menu()
    assert r == {"errcode": 0, "errmsg": "ok"}

    try:
        client.create_menu({"error": "error"})
    except ClientException as e:
        assert str(e) == "1: error"
