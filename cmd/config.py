from typing import Dict


def parse_config(args: Dict[str, bool]) -> None:
    if args['user']:
        user_config()
    if args['template']:
        template_config()


def user_config():
    pass


def template_config():
    pass
