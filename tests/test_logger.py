import time
import logging

from werobot.logger import enable_pretty_logging, _LogFormatter


def get_new_logger():
    return logging.getLogger(str(time.time()))


def test_logger_level():
    for level in ('debug', 'info', 'warning', 'error'):
        logger = get_new_logger()
        enable_pretty_logging(logger, level=level)
        assert logger.level == getattr(logging, level.upper())


def test_handlers():
    logger = get_new_logger()
    enable_pretty_logging(logger)
    assert isinstance(logger.handlers[0].formatter, _LogFormatter)
