# -*- coding: utf-8 -*-

from werobot.session import SessionStorage
from werobot.utils import json_loads, json_dumps
import sqlite3

__CREATE_TABLE_SQL__ = """
CREATE TABLE IF NOT EXISTS WeRoBot
(id TEXT PRIMARY KEY NOT NULL ,
value TEXT NOT NULL );
"""


class SQLiteStorage(SessionStorage):
    """
    SQLiteStorge 会把 Session 数据储存在一个 SQLite 数据库文件中 ::

        import werobot
        from werobot.session.sqlitestorage import SQLiteStorage

        session_storage = SQLiteStorage
        robot = werobot.WeRoBot(token="token", enable_session=True,
                                session_storage=session_storage)

    :param filename: SQLite数据库的文件名, 默认是 ``werobot_session.sqlite3``
    """
    def __init__(self, filename='werobot_session.sqlite3'):
        self.db = sqlite3.connect(filename, check_same_thread=False)
        self.db.text_factory = str
        self.db.execute(__CREATE_TABLE_SQL__)

    def get(self, id):
        """
        根据 id 获取数据。

        :param id: 要获取的数据的 id
        :return: 返回取到的数据，如果是空则返回一个空的 ``dict`` 对象
        """
        session_json = self.db.execute(
            "SELECT value FROM WeRoBot WHERE id=? LIMIT 1;", (id, )
        ).fetchone()
        if session_json is None:
            return {}
        return json_loads(session_json[0])

    def set(self, id, value):
        """
        根据 id 写入数据。

        :param id: 要写入的 id
        :param value: 要写入的数据，可以是一个 ``dict`` 对象
        """
        self.db.execute(
            "INSERT OR REPLACE INTO WeRoBot (id, value) VALUES (?,?);",
            (id, json_dumps(value))
        )
        self.db.commit()

    def delete(self, id):
        """
        根据 id 删除数据。

        :param id: 要删除的数据的 id
        """
        self.db.execute("DELETE FROM WeRoBot WHERE id=?;", (id, ))
        self.db.commit()
