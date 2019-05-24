#! /usr/bin/env python3
"""
cp-helper - Competitive programming tool.

Usage:
  cf-helper.py (-v|--version)
  cf-helper.py (-h|--help)
  cf-helper.py config user
  cf-helper.py config template (add|delete|default)
  cf-helper.py config print

Options:
  -v --version  Show version.
  -h --help     Show this screen.
"""
from docopt import docopt

import cmd

if __name__ == '__main__':
    arguments = docopt(__doc__, version="Developer pre-alpha-0.0.1")
    cmd.parse_args(arguments)
