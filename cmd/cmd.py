import typing

from .config import parse_config


def parse_args(args: typing.Dict[str, bool]) -> None:
    if args['config']:
        parse_config(args)
