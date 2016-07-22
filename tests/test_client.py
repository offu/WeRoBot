import os

from werobot.config import Config
from werobot.client import Client

basedir = os.path.dirname(os.path.abspath(__file__))

APP_ID = "123"
APP_SECRET = "321"


def test_id_and_secret():
    config = Config()
    config.from_pyfile(os.path.join(basedir, "test_client.py"))
    client = Client(config)
    assert client.appid == "123"
    assert client.appsecret == "321"
