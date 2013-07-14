from . import SessionStorage
from werobot.utils import json_loads, json_dumps


class RedisStorage(SessionStorage):
    def __init__(self, redis, prefix='werobot_session_'):
        for method_name in ['get', 'set', 'delete']:
            assert hasattr(redis, method_name)
        self.redis = redis
        self.prefix = prefix

    def key_name(self, s):
        return '{prefix}{s}'.format(prefix=self.prefix, s=s)

    def get(self, id):
        id = self.key_name(id)
        session_json = self.redis.get(id)
        return json_loads(session_json)

    def set(self, id, value):
        id = self.key_name(id)
        self.redis.set(json_dumps(value))

    def delete(self, id):
        id = self.key_name(id)
        self.redis.delte(id)
