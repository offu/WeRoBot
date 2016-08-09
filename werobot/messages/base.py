class WeRoBotMetaClass(type):
    TYPES = {}

    def __new__(mcs, name, bases, attrs):
        return type.__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        if '__type__' in attrs:
            if isinstance(attrs['__type__'], list):
                for _type in attrs['__type__']:
                    cls.TYPES[_type] = cls
            else:
                cls.TYPES[attrs['__type__']] = cls
        type.__init__(cls, name, bases, attrs)
