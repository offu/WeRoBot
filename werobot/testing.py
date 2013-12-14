from .parser import parse_user_msg

__all__ = ['WeTest']


class WeTest(object):
    def __init__(self, app):
        self._app = app

    def send_xml(self, xml):
        message = parse_user_msg(xml)
        return self._app.get_reply(message)
