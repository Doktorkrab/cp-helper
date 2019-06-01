from client.test import run_test
from .config import parse_config
from .contest import parse_fetch, parse_submit
from .utils import find_code
from utils import color


def parse_args(args: dict) -> None:
    if args['config']:
        parse_config(args)
    if args['fetch']:
        parse_fetch(args)
    if args['test']:
        ret = find_code(args)
        if ret is None:
            print(color("Can't find any file.", fg='Red', bright_fg=True))
            return
        run_test(ret[0], ret[1])
    if args['submit']:
        parse_submit(args)
