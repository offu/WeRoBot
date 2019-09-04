# -*- coding: utf-8 -*-

import types


class ConfigAttribute(object):
    """
    让一个属性指向一个配置
    """
    def __init__(self, name):
        self.__name__ = name

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        rv = obj.config[self.__name__]
        return rv

    def __set__(self, obj, value):
        obj.config[self.__name__] = value


class Config(dict):
    def from_pyfile(self, filename):
        """
        在一个 Python 文件中读取配置。

        :param filename: 配置文件的文件名
        :return: 如果读取成功，返回 ``True``，如果失败，会抛出错误异常
        """
        d = types.ModuleType('config')
        d.__file__ = filename
        with open(filename) as config_file:
            exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        self.from_object(d)
        return True

    def from_object(self, obj):
        """
        在给定的 Python 对象中读取配置。

        :param obj: 一个 Python 对象
        """
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
