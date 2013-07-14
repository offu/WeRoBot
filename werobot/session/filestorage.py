import json

try:
    import anydbm as dbm
    assert dbm
except ImportError:
    import dbm

from . import SessionStorage
from werobot.utils import py3k


class FileStorage(SessionStorage):
    def __init__(self, filename='werobot_session'):
        self.db = dbm.open(filename, "c")

    def get(self, id):
        session_json = self.db.get(id, "{}")
        if py3k:
            session_json = session_json.decode()
        return json.loads(session_json)

    def set(self, id, value):
        self.db[id] = json.dumps(value)

    def delete(self, id):
        del self.db[id]
