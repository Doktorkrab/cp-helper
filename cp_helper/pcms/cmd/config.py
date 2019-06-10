from getpass import getpass
from os import makedirs, listdir
from os.path import expanduser, isfile
from shutil import get_terminal_size

from requests import get

from cp_helper.pcms.config.core import Config
from cp_helper.utils import color, choose_yn

CONFIG_PATH = expanduser('~/.cpConfigPcms/')


def parse_config(args: dict) -> None:
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
    elif args['new']:
        new_config(args)
    elif args['template']:
        template_parse(args)


def new_config(args: dict) -> None:
    path = CONFIG_PATH + args['<config-name>']
    if isfile(path) and not choose_yn(f'Config {args["<config-name>"]} existed. Rewrite?'):
        return

    cfg = Config(path)
    cfg.url = input('URL:')
    resp = get(cfg.url)
    while (resp.status_code != 200 and resp.status_code != 302) or not resp.url.endswith('login.xhtml'):
        cfg.url = input('Enter a right pcms url:')
        resp = get(cfg.url)

    username = input('Username:')
    password = getpass('Password:')

    cfg.login(username, password)


def template_parse(args: dict) -> None:
    path = CONFIG_PATH + args['<config-name>']
    if not isfile(path):
        print(color('Config not found.', fg='red', bright_fg=True))
        return

    cfg = Config(path)
    if args['add']:
        cfg.add_template()
    if args['delete']:
        cfg.delete_template()
