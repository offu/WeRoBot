import sys
import re
import random
import time
import logging
import json
import six

try:
    import curses
    assert curses
except ImportError:
    curses = None

string_types = (six.string_types, six.text_type, six.binary_type)


def check_token(token):
    return re.match('^[A-Za-z0-9]{3,32}$', token)


def to_text(value, encoding="utf-8"):
    if isinstance(value, (six.string_types, six.binary_type)):
        return value.decode(encoding)
    if isinstance(value, int):
        return six.text_type(value)
    assert isinstance(value, six.text_type)
    return value


def to_binary(value, encoding="utf-8"):
    if isinstance(value, six.text_type):
        return value.encode(encoding)
    if isinstance(value, int):
        return six.binary_type(value)
    assert isinstance(value, six.binary_type)
    return value


def is_string(value):
    return isinstance(value, string_types)


def generate_token(length=''):
    if not length:
        length = random.randint(3, 32)
    length = int(length)
    assert 3 <= length <= 32
    token = []
    letters = 'abcdefghijklmnopqrstuvwxyz' \
              'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
              '0123456789'
    for _ in range(length):
        token.append(random.choice(letters))
    return ''.join(token)


def enable_pretty_logging(logger, level='info'):
    """Turns on formatted logging output as configured.
    """
    logger.setLevel(getattr(logging, level.upper()))

    if not logger.handlers:
        # Set up color if we are in a tty and curses is installed
        color = False
        if curses and sys.stderr.isatty():
            try:
                curses.setupterm()
                if curses.tigetnum("colors") > 0:
                    color = True
            except:
                pass
        channel = logging.StreamHandler()
        channel.setFormatter(_LogFormatter(color=color))
        logger.addHandler(channel)


class _LogFormatter(logging.Formatter):
    def __init__(self, color, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)
        self._color = color
        if color:
            # The curses module has some str/bytes confusion in
            # python3.  Until version 3.2.3, most methods return
            # bytes, but only accept strings.  In addition, we want to
            # output these strings with the logging module, which
            # works with unicode strings.  The explicit calls to
            # unicode() below are harmless in python2 but will do the
            # right conversion in python 3.
            fg_color = (curses.tigetstr("setaf") or
                        curses.tigetstr("setf") or "")
            if (3, 0) < sys.version_info < (3, 2, 3):
                fg_color = unicode(fg_color, "ascii")
            self._colors = {
                logging.DEBUG: unicode(curses.tparm(fg_color, 4),
                                       "ascii"),  # Blue
                logging.INFO: unicode(curses.tparm(fg_color, 2),
                                      "ascii"),  # Green
                logging.WARNING: unicode(curses.tparm(fg_color, 3),
                                         "ascii"),  # Yellow
                logging.ERROR: unicode(curses.tparm(fg_color, 1),
                                       "ascii"),  # Red
            }
            self._normal = unicode(curses.tigetstr("sgr0"), "ascii")

    def format(self, record):
        try:
            record.message = record.getMessage()
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)
        record.asctime = time.strftime(
            "%y%m%d %H:%M:%S", self.converter(record.created))
        prefix = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]' % \
                 record.__dict__
        if self._color:
            prefix = (self._colors.get(record.levelno, self._normal) +
                      prefix + self._normal)
        formatted = prefix + " " + record.message
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            formatted = formatted.rstrip() + "\n" + record.exc_text
        return formatted.replace("\n", "\n    ")


def json_loads(s):
    s = to_text(s)
    return json.loads(s)


def json_dumps(d):
    return json.dumps(d)
