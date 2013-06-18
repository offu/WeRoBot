#!/usr/bin/env python
# -*- coding: utf-8 -*-


class WebotException(Exception):
    pass


class UnknownMessageType(WebotException):
    pass


class HandlerNotFound(WebotException):
    pass
