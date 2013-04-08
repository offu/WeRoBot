import sys
import re
import random

try:
    import curses
except ImportError:
    curses = None

py = sys.version_info
py3k = py >= (3, 0, 0)

if py3k:
    basestring = str
    unicode = str


def check_token(token):
    return re.match('^[A-Za-z0-9]{3,32}$', token)


def to_unicode(value):
    if isinstance(value, unicode):
        return value
    if isinstance(value, basestring):
        return value.decode('utf-8')
    if isinstance(value, int):
        return str(value)
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return value


def isstring(value):
    return isinstance(value, basestring)


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