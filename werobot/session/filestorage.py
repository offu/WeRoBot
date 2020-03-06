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
    def __init__(self, filename: str = 'werobot_session'):
        try:
            self.db = dbm.open(filename, "c")
        except TypeError:  # pragma: no cover
            # dbm in PyPy requires filename to be binary
            self.db = dbm.open(to_binary(filename), "c")

    def get(self, id):
        """
        根据 id 获取数据。

        :param id: 要获取的数据的 id
        :return: 返回取到的数据，如果是空则返回一个空的 ``dict`` 对象
        """
        try:
            session_json = self.db[id]
        except KeyError:
            session_json = "{}"
        return json_loads(session_json)

    def set(self, id, value):
        """
        根据 id 写入数据。

        :param id: 要写入的 id
        :param value: 要写入的数据，可以是一个 ``dict`` 对象
        """
        self.db[id] = json_dumps(value)

    def delete(self, id):
        """
        根据 id 删除数据。

        :param id: 要删除的数据的 id
        """
        del self.db[id]
