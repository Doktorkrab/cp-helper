from os.path import expanduser

home = expanduser("~")
CONFIG_PATH = home + '/.cpConfig'
SESSION_PATH = home + '/.cpSession'

from .config import Config
from .langs import LangList

__all__ = ['config', 'langs']
