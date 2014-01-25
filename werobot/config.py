# -*- coding: utf-8 -*-

import imp


class Config(dict):
    def from_pyfile(self, filename):
        """
        在一个 Python 文件中读取配置。

        :param filename: 配置文件的文件名。
        """
        d = imp.new_module('config')
        d.__file__ = filename
        with open(filename) as config_file:
            exec (compile(config_file.read(), filename, 'exec'), d.__dict__)
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
