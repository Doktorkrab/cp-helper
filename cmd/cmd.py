from client.test import run_test
from .config import parse_config
from .contest import parse_fetch


def parse_args(args: dict) -> None:
    if args['config']:
        parse_config(args)
    if args['fetch']:
        parse_fetch(args)
    if args['test']:
        run_test(args['<filename>'])
