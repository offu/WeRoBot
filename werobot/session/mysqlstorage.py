# -*- coding: utf-8 -*-
import re

from werobot.session import SessionStorage
from werobot.utils import json_loads, json_dumps


__CREATE_TABLE_SQL__ = """
CREATE TABLE IF NOT EXISTS WeRoBot(
id VARCHAR(100) NOT NULL ,
value VARCHAR(1000) NOT NULL,
PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


class MySQLStorage(SessionStorage):
    """
    MySQLStorage 会把你的 Session 数据储存在 MySQL 中 ::

        import MySQLdb
        import werobot
        from werobot.session.mysqlstorage import MySQLStorage

        conn = MySQLdb.connect(user='', db='', passwd='', host='')
        session_storage = MySQLStorage(conn)
        robot = werobot.WeRoBot(token="token", enable_session=True,
                                session_storage=session_storage)


    python3 你需要安装 ``mysqlclient`` 才能使用 MySQLdb 。

    :param
    """

    def __init__(self, conn):
        """
        1. 通过获取到数据库连接conn下的cursor() 方法来创建游标 cur
        2. 创建数据表，通过游标cur操作execute()方法可以写入sql语句
        """
        self.conn = conn
        self.conn.cursor().execute(__CREATE_TABLE_SQL__)

    def get(self, id):
        """
        根据 id 获取数据。

        :param id: 要获取的数据的 id
        :return: 返回一个 ``dict`` 对象
        """
        session_tuple = None
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT value FROM WeRoBot WHERE id='%s' LIMIT 1" % (id,))  # execute返回select的数目
            session_tuple = cur.fetchone()  # 返回单个的元组，也就是一条记录(row)，如果没有结果 则返回 None
        except:
            self.conn.rollback()  # 发生错误时回滚

        if session_tuple is None:
            return {}
#        session_dict = {id: session_tuple[0]}  #构建返回的 ``dict`` 对象
        session_dict = session_tuple[0]  # assert storage.get("喵") == u"喵喵" 这测试不是 dict 啊，大哥
#        session_dict = re.sub("'", "\"", str(session_dict))  # 将字符串里的单引号替换成双引号，否则json.loads报错
#        return json_loads(session_dict)  # 测试不通过
        return session_dict

    def set(self, id, value):
        """
        根据 id 写入数据。

        :param id: 要写入的 id
        :param value: 要写入的数据，一个 ``dict`` 对象
        """
        sql = "INSERT INTO WeRoBot (id, value) VALUES ('%s','%s') ON DUPLICATE KEY UPDATE value='%s'" % (id, value, value)
        try:
            # 执行sql语句
            self.conn.cursor().execute(sql)
            # 提交到数据库执行
            self.conn.commit()
        except:
            # 发生错误时回滚
            self.conn.rollback()

    def delete(self, id):
        """
        根据 id 删除数据。

        :param id: 要删除的数据的 id
        """
        try:
            self.conn.cursor().execute("DELETE FROM WeRoBot WHERE id='%s'" % (id,))
            # 提交到数据库执行
            self.conn.commit()
        except:
            # 发生错误时回滚
            self.conn.rollback()
