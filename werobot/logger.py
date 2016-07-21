# -*- coding:utf-8 -*-

import six
import sys
import time
import logging

try:
    import curses

    assert curses
except ImportError:
    curses = None

logger = logging.getLogger("WeRoBot")


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
            fg_color = (curses.tigetstr("setaf") or
                        curses.tigetstr("setf") or "")
            if (3, 0) < sys.version_info < (3, 2, 3):
                fg_color = six.text_type(fg_color, "ascii")
            self._colors = {
                logging.DEBUG: six.text_type(
                    curses.tparm(fg_color, 4),
                    "ascii"
                ),  # Blue
                logging.INFO: six.text_type(
                    curses.tparm(fg_color, 2),
                    "ascii"
                ),  # Green
                logging.WARNING: six.text_type(
                    curses.tparm(fg_color, 3),
                    "ascii"
                ),  # Yellow
                logging.ERROR: six.text_type(
                    curses.tparm(fg_color, 1),
                    "ascii"
                ),  # Red
            }
            self._normal = six.text_type(curses.tigetstr("sgr0"), "ascii")

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
