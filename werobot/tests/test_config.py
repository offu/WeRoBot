import os

basedir = os.path.dirname(os.path.abspath(__file__))

from werobot import WeRoBot
from werobot.config import Config
from werobot.utils import generate_token
from werobot.client import Client

APP_ID = "123"
APP_SECRET="321"


def test_from_pyfile():
    config = Config()
    assert "TOKEN" not in config
    config.from_pyfile(os.path.join(basedir, "test_config.py"))
    assert config["APP_SECRET"] == "321"
    client=Client(config)
    assert client.appsecret == "321"
    assert client.appid == "123"



def test_from_object():
    config = Config()
    config.from_pyfile(os.path.join(basedir, "test_config.py"))

    class ConfigObject():
        APP_ID = "456"
    config.from_object(ConfigObject())
    assert config["APP_ID"] == "456"


def test_config_attribute():
    robot = WeRoBot()
    assert not robot.token
    token = generate_token()
    robot.config["TOKEN"] = token
    assert robot.token == token

    token = generate_token()
    robot.token = token
    assert robot.config["TOKEN"] == token

"""
if __name__=="__main__":
    test_config_attribute()
    test_from_object()
    test_from_pyfile()
"""