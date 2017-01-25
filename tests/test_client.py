import os
import responses
import json

from werobot import WeRoBot
from werobot.config import Config
from werobot.client import Client, check_error, ClientException

basedir = os.path.dirname(os.path.abspath(__file__))

APP_ID = "123"
APP_SECRET = "321"

TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"


def token_callback(request):
    headers = {'content-type': 'application/json'}
    return 200, headers, json.dumps({"access_token": "ACCESS_TOKEN", "expires_in": 7200})


def test_id_and_secret():
    config = Config()
    config.from_pyfile(os.path.join(basedir, "test_client.py"))
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
    config.from_pyfile(os.path.join(basedir, "test_client.py"))
    client = Client(config)

    client.grant_token()
    assert client.token == "ACCESS_TOKEN"


@responses.activate
def test_client_request():
    EMPTY_PARAMS_URL = "http://empty-params.werobot.com/"
    DATA_EXISTS_URL = "http://data-exists.werobot.com/"

    def empty_params_callback(request):
        assert request.url[request.url.rfind("=") + 1:] == client.token
        headers = {'content-type': 'application/json'}
        return 200, headers, json.dumps({"test": "test"})

    def data_exists_url(request):
        assert json.loads(request.body.decode('utf-8')) == {"test": "test"}
        headers = {'content-type': 'application/json'}
        return 200, headers, json.dumps({"test": "test"})

    responses.add_callback(responses.POST, DATA_EXISTS_URL, callback=data_exists_url)
    responses.add_callback(responses.GET, EMPTY_PARAMS_URL, callback=empty_params_callback)
    responses.add_callback(responses.GET, TOKEN_URL, callback=token_callback)

    config = Config()
    config.from_pyfile(os.path.join(basedir, "test_client.py"))
    client = Client(config)

    r = client.get(url=EMPTY_PARAMS_URL)
    assert r == {"test": "test"}

    r = client.post(url=DATA_EXISTS_URL, data={"test": "test"})
    assert r == {"test": "test"}
