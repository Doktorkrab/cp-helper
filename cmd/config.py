from typing import Dict

import config


def parse_config(args: Dict[str, bool]) -> None:
    if args['user']:
        user_config(args)
    if args['template']:
        template_config(args)
    if args['print']:
        cfg = config.Config()
        print(cfg)
    if args['cf_api']:
        cf_api(args)
    if args['lang']:
        lang(args)


def user_config(args: Dict[str, bool]) -> None:
    cfg = config.Config()
    cfg.modify_user()


def template_config(args: Dict[str, bool]) -> None:
    cfg = config.Config()
    if args['add']:
        cfg.add_template()
    if args['delete']:
        cfg.delete_template()
    if args['default']:
        cfg.set_default_template()


def cf_api(args: Dict[str, bool]) -> None:
    cfg = config.Config()
    cfg.key = args['<key>']
    cfg.secret = args['<secret>']
    cfg.save()


def lang(args: Dict[str, bool]) -> None:
    cfg = config.Config()
    print(f'Now locale is {cfg.lang}')
    now = ''
    while now != 'ru' and now != 'en':
        now = input('Enter locale(en or ru):')
    cfg.lang = now
    cfg.save()
