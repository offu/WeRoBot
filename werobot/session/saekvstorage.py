# -*- coding: utf-8 -*-

from . import SessionStorage


class SaeKVDBStorage(SessionStorage):
    """
    SaeKVDBStorage 使用SAE 的 KVDB 来保存你的session ::

        import werobot
        from werobot.session.saekvstorage import SaeKVDBStorage

        session_storage = SaeKVDBStorage()
        robot = werobot.WeRoBot(token="token", enable_session=True,
                                session_storage=session_storage)

    需要先在后台开启 KVDB 支持

    :param prefix: KVDB 中 Session 数据 key 的 prefix 。默认为 ``ws_``
    """
    def __init__(self, prefix='ws_'):
        try:
            import sae.kvdb
        except ImportError:
            raise RuntimeError("SaeKVDBStorage requires SAE environment")
        self.kv = sae.kvdb.KVClient()
        self.prefix = prefix

    def key_name(self, s):
        return '{prefix}{s}'.format(prefix=self.prefix, s=s)

    def get(self, id):
        return self.kv.get(self.key_name(id)) or {}

    def set(self, id, value):
        return self.kv.set(self.key_name(id), value)

    def delete(self, id):
        return self.kv.delete(self.key_name(id))
