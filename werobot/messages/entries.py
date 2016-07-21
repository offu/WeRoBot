# -*- coding: utf-8 -*-
from werobot.utils import to_text


class BaseEntry(object):
    def __init__(self, entry, default=None):
        self.entry = entry
        self.default = default


class IntEntry(BaseEntry):
    def __get__(self, instance, owner):
        try:
            v = int(instance.__dict__.get(self.entry, self.default))
        except TypeError:
            v = None
        return v


class FloatEntry(BaseEntry):
    def __get__(self, instance, owner):
        try:
            v = float(instance.__dict__.get(self.entry, self.default))
        except TypeError:
            v = None
        return v


class StringEntry(BaseEntry):
    def __get__(self, instance, owner):
        v = instance.__dict__.get(self.entry, self.default)
        if v is not None:
            return to_text(v)
        return v
