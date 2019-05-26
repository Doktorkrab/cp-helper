import typing

from .config import parse_config
from .contest import parse_fetch


def parse_args(args: typing.Dict[str, str]) -> None:
    if args['config']:
        parse_config(args)
    if args['fetch']:
        parse_fetch(args)
