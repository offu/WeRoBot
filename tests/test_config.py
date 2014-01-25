import os

basedir = os.path.dirname(os.path.abspath(__file__))

from werobot.config import Config


TOKEN = "123"


def test_from_pyfile():
    config = Config()
    assert "TOKEN" not in config
    config.from_pyfile(os.path.join(basedir, "test_config.py"))
    assert config["TOKEN"] == "123"


def test_from_object():
    config = Config()
    config.from_pyfile(os.path.join(basedir, "test_config.py"))

    class ConfigObject():
        TOKEN = "456"
    config.from_object(ConfigObject())
    assert config["token"] == "456"