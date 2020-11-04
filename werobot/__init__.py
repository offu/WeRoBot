__version__ = '1.13.0'
__author__ = 'whtsky'
__license__ = 'MIT'

__all__ = ["WeRoBot"]

try:
    from werobot.robot import WeRoBot
except ImportError:  # pragma: no cover
    pass  # pragma: no cover
