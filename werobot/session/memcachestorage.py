# -*- coding: utf-8 -*-

from werobot.session import SessionStorage
from werobot.utils import json_loads, json_dumps


class MemcacheStorage(SessionStorage):
    """
        MemcacheStorage 会把你的 Session 数据储存在 Memcache 中 ::

            import memcache
            import werobot
            from werobot.session.memcachestorage import MemcacheStorage

            db = memcache.Client(['127.0.0.1:12000'],debug=0)
            session_storage = MemcacheStorage(db, prefix="my_prefix_")
            robot = werobot.WeRoBot(token="token", enable_session=True,
                                    session_storage=session_storage)


        你需要安装 ``memcache`` 才能使用 MemcacheStorage 。

        :param memcache: 一个 memcache Client。
        :param prefix: memcache 中 Session 数据 key 的 prefix 。默认为 ``ws_``
        """
    def __init__(self, memcache, prefix='ws_'):
        self.memcache = memcache
        self.prefix = prefix

    def key_name(self, s):
        return '{prefix}{s}'.format(prefix=self.prefix, s=s)

    def get(self, id):
        id = self.key_name(id)
        session_json = self.memcache.get(id) or '{}'
        return json_loads(session_json)

    def set(self, id, value):
        id = self.key_name(id)
        self.memcache.set(id, json_dumps(value))

    def delete(self, id):
        id = self.key_name(id)
        self.memcache.delete(id)
