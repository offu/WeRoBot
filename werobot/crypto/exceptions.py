# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class UnvalidEncodingAESKey(Exception):
    pass


class AppIdValidationError(Exception):
    pass


class InvalidSignature(Exception):
    pass
