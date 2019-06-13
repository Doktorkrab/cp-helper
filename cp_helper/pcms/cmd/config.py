from getpass import getpass
from os import listdir, makedirs
from os.path import isdir
from shutil import get_terminal_size

from requests import get

from cp_helper.pcms.client.contest import get_contests_list, get_contest_langs, get_contest_status
from cp_helper.pcms.client.core import Client
from cp_helper.pcms.config import CONFIG_PATH
from cp_helper.pcms.config.core import Config
from cp_helper.utils import color, choose_yn


def parse_config(args: dict) -> None:
    makedirs(CONFIG_PATH, exist_ok=True)

    if args['print']:
        if args['<config-name>']:
            path = f'{CONFIG_PATH}/{args["<config-name>"]}'
            if not isdir(path):
                print(color('Config not found.', fg='red', bright_fg=True))
                return
            cfg = Config(args['<config-name>'])
            print(cfg)
        else:
            configs = listdir(CONFIG_PATH)
            cnt = 0
            for config in configs:
                if not isdir(f'{CONFIG_PATH}/{config}') or 'config' not in listdir(f'{CONFIG_PATH}/{config}'):
                    continue
                cfg = Config(config)
                if cnt:
                    print('-' * get_terminal_size().columns)
                cnt += 1
                print(cfg)
    elif args['new']:
        new_config(args)
    elif args['template']:
        template_parse(args)
    elif args['update']:
        update_langs(args)


def new_config(args: dict) -> None:
    path = f'{CONFIG_PATH}/{args["<config-name>"]}'
    if isdir(path) and not choose_yn(f'Config {args["<config-name>"]} existed. Rewrite?'):
        return

    cfg = Config(args['<config-name>'])
    cfg.url = input('URL:')
    resp = get(cfg.url)
    cfg.url = resp.url
    while (resp.status_code != 200 and resp.status_code != 302) or not resp.url.endswith('login.xhtml'):
        cfg.url = input('Enter a right pcms url:')
        resp = get(cfg.url)
        cfg.url = resp.url

    cfg.url = cfg.url.replace('login.xhtml', '')
    username = input('Username:')
    password = getpass('Password:')

    cfg.login(username, password)

    update_langs(args)


def update_langs(args: dict):
    path = f'{CONFIG_PATH}/{args["<config-name>"]}'
    if not isdir(path):
        print(color('Config not found.', fg='red', bright_fg=True))
        return
    cfg = Config(args['<config-name>'])
    cl = Client(args['<config-name>'])
    session = cl.session

    contests = get_contests_list(args['<config-name>'])
    cfg.langs = []
    for contest in contests:
        if contest.url:
            url = cfg.url + contest.url[contest.url.index('party'):]
            resp = session.get(url)
            if resp.status_code != 200 and resp.status_code != 302:
                print(contest.id, '...', color(f'UNKNOWN: {resp.status_code}', fg='magenta', bright_fg=True))
                continue
        status, virt = get_contest_status(args['<config-name>'])
        contest.virtual = virt
        status_color = ''
        if 'RUNNING' in status:
            status_color = 'green'
        elif 'OVER' in status:
            status_color = 'yellow'
        elif "BEFORE" in status:
            status_color = 'blue'

        if virt:
            status = status.rstrip() + ' (Virtual)'
        print(contest.id, '...', color(status, fg=status_color, bright_fg=True))
        cfg.langs = list(set(cfg.langs) | set(get_contest_langs(args['<config-name>'])))


def template_parse(args: dict) -> None:
    path = f'{CONFIG_PATH}/{args["<config-name>"]}'
    if not isdir(path):
        print(color('Config not found.', fg='red', bright_fg=True))
        return

    cfg = Config(args['<config-name>'])
    if args['add']:
        cfg.add_template()
    if args['delete']:
        cfg.delete_template()
