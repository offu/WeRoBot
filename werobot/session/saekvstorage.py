# -*- coding: utf-8 -*-

from . import SessionStorage

import sae.kvdb


class SaeKVDBStorage(SessionStorage):
    """
    SaeKVDBStorage 使用SAE 的 KVDB 来保存你的session
    
    需要先在后台开启 KVDB 支持

    from werobot.session.saekvstorage import SaeKVDBStorage

    session_storage = SaeKVDBStorage()
    robot = werobot.WeRoBot(token="token", enable_session=True,
                            session_storage=session_storage)

    """
    def __init__(self, prefix='WESESSION'):
        self.kv = sae.kvdb.KVClient()
        self.prefix = prefix

    def prefixid(self, id):
        return self.prefix + str(id)

    def get(self, id):
        return self.kv.get(self.prefixid(id)) or {}

    def set(self, id, value):
        return self.kv.set(self.prefixid(id), value)

    def delete(self, id):
        return self.kv.delete(self.prefixid(id))

