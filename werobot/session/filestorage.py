# -*- coding: utf-8 -*-

try:
    import anydbm as dbm

    assert dbm
except ImportError:
    import dbm

from werobot.session import SessionStorage
from werobot.utils import json_loads, json_dumps, to_binary


class FileStorage(SessionStorage):
    """
    FileStorage 会把你的 Session 数据以 dbm 形式储存在文件中。

    :param filename: 文件名， 默认为 ``werobot_session``
    """

    def __init__(self, filename='werobot_session'):
        try:
            self.db = dbm.open(filename, "c")
        except TypeError:
            # dbm in PyPy requires filename to be binary
            self.db = dbm.open(to_binary(filename), "c")

    def get(self, id):
        try:
            session_json = self.db[id]
        except KeyError:
            session_json = "{}"
        return json_loads(session_json)

    def set(self, id, value):
        self.db[id] = json_dumps(value)

    def delete(self, id):
        del self.db[id]
