# -*- coding: utf-8 -*-

try:
    import anydbm as dbm
    assert dbm
except ImportError:
    import dbm

from werobot.session import SessionStorage
from werobot.utils import json_loads, json_dumps


class FileStorage(SessionStorage):
    """
    FileStorage 会把你的 Session 数据以 dbm 形式储存在文件中。

    :param filename: 文件名， 默认为 ``werobot_session``
    """
    def __init__(self, filename='werobot_session'):
        self.db = dbm.open(filename, "c")

    def get(self, id):
        session_json = self.db.get(id, "{}")
        return json_loads(session_json)

    def set(self, id, value):
        self.db[id] = json_dumps(value)

    def delete(self, id):
        del self.db[id]
