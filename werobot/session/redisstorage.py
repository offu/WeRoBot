# -*- coding: utf-8 -*-

from werobot.session import SessionStorage
from werobot.utils import json_loads, json_dumps


class RedisStorage(SessionStorage):
    """
    RedisStorage 会把你的 Session 数据储存在 Redis 中 ::

        import redis
        import werobot
        from werobot.session.redisstorage import RedisStorage

        db = redis.Redis()
        session_storage = RedisStorage(db, prefix="my_prefix_")
        robot = werobot.WeRoBot(token="token", enable_session=True,
                                session_storage=session_storage)


    你需要安装 ``redis`` 才能使用 RedisStorage 。

    :param redis: 一个 Redis Client。
    :param prefix: Reids 中 Session 数据 key 的 prefix 。默认为 ``ws_``
    """
    def __init__(self, redis, prefix='ws_'):
        for method_name in ['get', 'set', 'delete']:
            assert hasattr(redis, method_name)
        self.redis = redis
        self.prefix = prefix

    def key_name(self, s):
        return '{prefix}{s}'.format(prefix=self.prefix, s=s)

    def get(self, id):
        id = self.key_name(id)
        session_json = self.redis.get(id) or '{}'
        return json_loads(session_json)

    def set(self, id, value):
        id = self.key_name(id)
        self.redis.set(id, json_dumps(value))

    def delete(self, id):
        id = self.key_name(id)
        self.redis.delete(id)
