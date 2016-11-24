import os

from werobot import WeRoBot
from werobot.config import Config
from werobot.utils import generate_token

basedir = os.path.dirname(os.path.abspath(__file__))

TOKEN = "123"


def test_from_pyfile():
    config = Config()
    assert "TOKEN" not in config
    config.from_pyfile(os.path.join(basedir, "test_config.py"))
    assert config["TOKEN"] == "123"


def test_from_object():
    config = Config()
    config.from_pyfile(os.path.join(basedir, "test_config.py"))

    class ConfigObject:
        TOKEN = "456"

    config.from_object(ConfigObject())
    assert config["TOKEN"] == "456"


def test_config_attribute():
    robot = WeRoBot(enable_session=False)
    assert not robot.token
    token = generate_token()
    robot.config["TOKEN"] = token
    assert robot.token == token

    token = generate_token()
    robot.token = token
    assert robot.config["TOKEN"] == token
