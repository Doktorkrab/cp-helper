import config


def parse_config(args: dict) -> None:
    if args['user']:
        user_config(args)
    elif args['template']:
        template_config(args)
    elif args['lang']:
        lang(args)
    else:
        cfg = config.Config()
        print(cfg)


def user_config(args: dict) -> None:
    cfg = config.Config()
    cfg.modify_user()


def template_config(args: dict) -> None:
    cfg = config.Config()
    if args['add']:
        cfg.add_template()
    if args['delete']:
        cfg.delete_template()
    if args['default']:
        cfg.set_default_template()


def lang(args: dict) -> None:
    cfg = config.Config()
    print(f'Now locale is {cfg.lang}')
    now = ''
    while now != 'ru' and now != 'en':
        now = input('Enter locale(en or ru):')
    cfg.lang = now
    cfg.save()
