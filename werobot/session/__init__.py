class SessionStorage(object):
    def get(self, id):
        raise NotImplementedError()

    def set(self, id, value):
        raise NotImplementedError()

    def delete(self, id):
        raise NotImplementedError()

    def __getitem__(self, id):
        return self.get(id)

    def __setitem__(self, id, session):
        self.set(id, session)

    def __delitem__(self, id):
        self.delete(id)
