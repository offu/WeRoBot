import json

try:
    import anydbm as dbm
    assert dbm
except ImportError:
    import dbm

from . import SessionStorage


class FileStorage(SessionStorage):
    def __init__(self, filename='werobot_session'):
        self.db = dbm.open(filename, "c")

    def get(self, id):
        return json.loads(self.db.get(id, "{}"))

    def set(self, id, value):
        self.db[id] = json.dumps(value)

    def delete(self, id):
        del self.db[id]
