from getpass import getpass
from os import listdir, makedirs, remove
from os.path import isdir, isfile
from shutil import get_terminal_size

from requests import Session

from cp_helper.pcms.client.contest import get_contests_list, get_contest_langs, Contest, get_contest_status
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
    elif args['switch']:
        switch(args)


def get_pcms_url(url: str):
    """
    Returns a url of pcms without /login, /logout, etc
    :param url: url to prettify
    :return: pretty url
    """
    ret = None
    print(url, ret)
    if ';' in url:
        url, ret = url.split(';')
    tmp = url.split('/')
    for i in range(len(tmp)):
        if tmp[i] == 'pcms2client':
            return '/'.join(tmp[:i + 1]), ret
    return None, ret


def new_config(args: dict) -> None:
    path = f'{CONFIG_PATH}/{args["<config-name>"]}'
    if isdir(path) and isfile(f'{path}/config'):
        if not choose_yn(f'Config {args["<config-name>"]} existed. Rewrite?'):
            return
        remove(f'{path}/config')
        if isfile(f'{path}/session'):
            remove(f'{path}/session')

    tmp_session = Session()
    tmp_session.headers.update({"User-Agent": "https://github.com/DoktorKrab/cp-helper"})

    cfg = Config(args['<config-name>'])
    cfg.url, shit = get_pcms_url(tmp_session.get((input('URL:'))).url)
    if shit is not None:
        tmp = shit.split('=')
        tmp_session.cookies[tmp[0]] = tmp[1]
    if cfg.url is not None:
        resp = tmp_session.get(cfg.url)
    else:
        resp = None
    while cfg.url is None or resp is None or (resp.status_code != 200 and resp.status_code != 302):
        cfg.url, shit = get_pcms_url(tmp_session.get((input('URL:'))).url)
        if shit is not None:
            tmp = shit.split('=')
            tmp_session.cookies[tmp[0]] = tmp[1]
        resp = tmp_session.get(cfg.url)
        cfg.url = resp.url

    # Save cookies. Thank you Innopolis
    cl = Client(args["<config-name>"])
    cl.cookies = tmp_session.cookies
    cl.save()

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
    contests = get_contests_list(cl)
    cur: Contest = cl.current_contest

    cfg.langs = []
    max_len = len(str(len(contests))) + 3
    for i in range(len(contests)):
        need_spaces = max_len - len(str(i + 1))
        contests[i].switch()
        print(f"{' ' * need_spaces}#{i + 1}{'' if contests[i] != cur else '(*)'}|{contests[i]}", end=', ')
        langs = get_contest_langs(cl)
        print(f'found {len(langs)} compilers')
        cfg.langs = list(set(cfg.langs) | set(langs))
    cur.switch()


def switch(args: dict):
    path = f'{CONFIG_PATH}/{args["<config-name>"]}'
    if not isdir(path):
        print(color('Config not found.', fg='red', bright_fg=True))
        return
    cl = Client(args['<config-name>'])
    print(get_contest_status(cl))
    contests = get_contests_list(cl)
    cur: Contest = cl.current_contest
    max_len = len(str(len(contests))) + 3

    for i in range(len(contests)):
        need_spaces = max_len - len(str(i + 1))
        contests[i].switch()
        print(f"{' ' * need_spaces}#{i + 1}{'' if contests[i] != cur else '(*)'}|{contests[i]}")
    num = input('Enter number:')
    while not num.isnumeric() or not (1 <= int(num) <= len(contests)):
        num = input('Enter number:')
    contests[int(num) - 1].switch()



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
