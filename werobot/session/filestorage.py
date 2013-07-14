try:
    import anydbm as dbm
    assert dbm
except ImportError:
    import dbm

from . import SessionStorage
from werobot.utils import json_loads, json_dumps


class FileStorage(SessionStorage):
    def __init__(self, filename='werobot_session'):
        self.db = dbm.open(filename, "c")

    def get(self, id):
        session_json = self.db.get(id, "{}")
        return json_loads(session_json)

    def set(self, id, value):
        self.db[id] = json_dumps(value)

    def delete(self, id):
        del self.db[id]
