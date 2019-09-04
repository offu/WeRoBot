# -*- coding: utf-8 -*-

from werobot.session import SessionStorage
from werobot.utils import json_loads, json_dumps

__CREATE_TABLE_SQL__ = """
CREATE TABLE IF NOT EXISTS WeRoBot(
id VARCHAR(100) NOT NULL ,
value BLOB NOT NULL,
PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""


class MySQLStorage(SessionStorage):
    """
    MySQLStorage 会把你的 Session 数据储存在 MySQL 中 ::

        import MySQLdb # 使用 mysqlclient
        import werobot
        from werobot.session.mysqlstorage import MySQLStorage

        conn = MySQLdb.connect(user='', db='', passwd='', host='')
        session_storage = MySQLStorage(conn)
        robot = werobot.WeRoBot(token="token", enable_session=True,
                                session_storage=session_storage)

    或者 ::

        import pymysql # 使用 pymysql
        import werobot
        from werobot.session.mysqlstorage import MySQLStorage

        session_storage = MySQLStorage(
        conn=pymysql.connect(
            user='喵',
            password='喵喵',
            db='werobot',
            host='127.0.0.1',
            charset='utf8'
        ))
        robot = werobot.WeRoBot(token="token", enable_session=True,
                                session_storage=session_storage)

    你需要安装一个 MySQL Client 才能使用 MySQLStorage，比如 ``pymysql``，``mysqlclient`` 。

    理论上符合 `PEP-249 <https://www.python.org/dev/peps/pep-0249/#connection-objects>`_ 的库都可以使用，\
    测试时使用的是 ``pymysql``。

    :param conn: `PEP-249 <https://www.python.org/dev/peps/pep-0249/#connection-objects>`_\
    定义的 Connection 对象
    """
    def __init__(self, conn):
        self.conn = conn
        self.conn.cursor().execute(__CREATE_TABLE_SQL__)

    def get(self, id):
        """
        根据 id 获取数据。

        :param id: 要获取的数据的 id
        :return: 返回取到的数据，如果是空则返回一个空的 ``dict`` 对象
        """
        cur = self.conn.cursor()
        cur.execute("SELECT value FROM WeRoBot WHERE id=%s LIMIT 1;", (id, ))
        session_json = cur.fetchone()
        if session_json is None:
            return {}
        return json_loads(session_json[0])

    def set(self, id, value):
        """
        根据 id 写入数据。

        :param id: 要写入的 id
        :param value: 要写入的数据，可以是一个 ``dict`` 对象
        """
        value = json_dumps(value)
        self.conn.cursor().execute(
            "INSERT INTO WeRoBot (id, value) VALUES (%s,%s) \
                ON DUPLICATE KEY UPDATE value=%s", (
                id,
                value,
                value,
            )
        )
        self.conn.commit()

    def delete(self, id):
        """
        根据 id 删除数据。

        :param id: 要删除的数据的 id
        """
        self.conn.cursor().execute("DELETE FROM WeRoBot WHERE id=%s", (id, ))
        self.conn.commit()
