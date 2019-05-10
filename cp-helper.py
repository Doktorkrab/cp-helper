#! /usr/bin/env python3
import sys
import typing

help_text = '''Competitive programming helper, version: 0.0.1'''


def parse_args(args: typing.List[str]) -> None:
    print(sys.argv)
    if len(args) < 2 or args[1] == 'help':
        print(help_text)
    elif args[1] == 'config':
        pass
    elif args[1] == 'submit':
        pass
    elif args[1] == 'race':
        pass
    elif args[1] == 'prepare':
        pass
    elif args[1] == 'parse':
        pass
    elif args[1] == 'test':
        pass
    else:
        print(help_text)


parse_args(sys.argv)
