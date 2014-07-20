__version__ = '0.6.0'
__author__ = 'whtsky'
__license__ = 'MIT'

__all__ = ["WeRoBot"]

try:
    from werobot.robot import WeRoBot
except ImportError:
    pass
