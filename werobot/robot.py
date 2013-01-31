import inspect
import hashlib
import tornado.web
import tornado.ioloop
import tornado.httpserver

from .parser import parse_user_msg
from .reply import create_reply
from .util import enable_pretty_logging


class WeRoBot(object):
    def __init__(self, token=''):
        self._handlers = []
        self.token = token

    def handler(self, func):
        """
        Decorator to add a new handler to the robot.
        """
        self._handlers.append(func)
        return func

    def add_handler(self, func):
        """
        Add a new handler to the robot.
        """
        if not inspect.isfunction(func):
            raise TypeError
        self._handlers.append(func)

    def _create_handler(robot):
        class WeChatHandler(tornado.web.RequestHandler):
            def prepare(self):
                signature = self.get_argument('signature', '')
                timestamp = self.get_argument('timestamp', '')
                nonce = self.get_argument('nonce', '')

                sign = [robot.token, timestamp, nonce]
                sign.sort()
                sign = ''.join(sign)
                sign = hashlib.sha1(sign).hexdigest()

                if sign is not signature:
                    self.finish()

            def get(self):
                echostr = self.get_argument('echostr', '')
                self.write(echostr)

            def post(self):
                body = self.request.body
                data = parse_user_msg(body)
                self.set_header("Content-Type",
                    "application/xml;charset=utf-8")
                for handler in robot._handlers:
                    reply = handler(data)
                    if reply:
                        self.write(create_reply(reply))
                        return
        return WeChatHandler

    def run(self, port=8888):
        WechatHandler = self._create_handler()
        enable_pretty_logging()
        app = tornado.web.Application([
            ('/', WechatHandler),
            ])
        server = tornado.httpserver.HTTPServer(app, xheaders=True)
        server.listen(int(port))
        tornado.ioloop.IOLoop.instance().start()
