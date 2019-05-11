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


def user_config(args: Dict[str, bool]) -> None:
    pass


def template_config(args: Dict[str, bool]) -> None:
    cfg = config.Config()
    if args['add']:
        cfg.add_template()
    if args['delete']:
        cfg.delete_template()
    if args['default']:
        cfg.set_default_template()
