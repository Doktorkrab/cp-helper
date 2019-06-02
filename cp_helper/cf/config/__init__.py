from os.path import expanduser

home = expanduser("~")
CONFIG_PATH = home + '/.cpConfig'
SESSION_PATH = home + '/.cpSession'

from .core import Config
from .langs import lang_list

__all__ = ['core', 'langs', Config]
