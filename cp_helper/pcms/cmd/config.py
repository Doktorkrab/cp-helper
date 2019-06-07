from os import makedirs, listdir
from os.path import expanduser, isfile
from shutil import get_terminal_size

from cp_helper.pcms.config.core import Config
from cp_helper.utils import color

CONFIG_PATH = expanduser('~/.cpConfigPcms/')


def parse_config(args: dict):
    makedirs(CONFIG_PATH, exist_ok=True)

    if args['print']:
        if args['<config-name>']:
            path = CONFIG_PATH + args['<config-name>']
            if not isfile(path):
                print(color('Invalid config name.', fg='red', bright_fg=True))
            cfg = Config(path)
            print(cfg)
        else:
            configs = listdir(CONFIG_PATH)
            cnt = 0
            for config in configs:
                cfg = Config(CONFIG_PATH + config)
                if cnt:
                    print('-' * get_terminal_size().columns)
                cnt += 1
                print(cfg)
