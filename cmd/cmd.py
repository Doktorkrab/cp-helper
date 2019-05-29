from client.test import run_test
from .config import parse_config
from .contest import parse_fetch, parse_submit
from .utils import find_code


def parse_args(args: dict) -> None:
    if args['config']:
        parse_config(args)
    if args['fetch']:
        parse_fetch(args)
    if args['test']:
        ret = find_code(args)
        if ret is None:
            print("Can't find any file.")
            return
        run_test(ret[0])
    if args['submit']:
        parse_submit(args)
