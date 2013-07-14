from . import SessionStorage
from werobot.utils import json_loads, json_dumps


class MongoDBStorage(SessionStorage):
    def __init__(self, collection):
        import pymongo
        assert isinstance(collection,
                          pymongo.collection.Collection)
        self.collection = collection
        collection.create_index("wechat_id")

    def _get_document(self, id):
        return self.collection.find_one({"wechat_id": id})

    def get(self, id):
        document = self._get_document(id)
        if document:
            session_json = document["session"]
            return json_loads(session_json)
        return {}

    def set(self, id, value):
        document = self._get_document(id)
        session = json_dumps(value)
        if document:
            document["session"] = session
            self.collection.save(document)
        else:
            self.collection.insert({
                "wechat_id": id,
                "session": session
            })

    def delete(self, id):
        document = self._get_document(id)
        if document:
            self.collection.remove(document["_id"])
