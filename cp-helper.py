# ! /usr/bin/env python3
"""
cp-helper - Competitive programming tool.

Usage:
  cf-helper.py
  cf-helper.py (-v|--version)
  cf-helper.py (-h|--help)

Options:
  -v --version  Show version.
  -h --help     Show this screen.
"""
import typing

from docopt import docopt


def parse_args(args: typing.Dict[str, bool]) -> None:
    pass


if __name__ == '__main__':
    arguments = docopt(__doc__, version="Developer pre-alpha-0.0.1")
    parse_args(arguments)
