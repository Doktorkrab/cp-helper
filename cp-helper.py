#! /usr/bin/env python3
"""
cp-helper - Competitive programming tool.

Usage:
  cp-helper.py (-v|--version)
  cp-helper.py (-h|--help)
  cp-helper.py config user
  cp-helper.py config template (add|delete|default)
  cp-helper.py config print
  cp-helper.py config cf_api <key> <secret>
  cp-helper.py config lang
  cp-helper.py fetch [(g <group-id>)] [<contest-id>] [<problem-id>]
  cp-helper.py test [<filename>]
  cp-helper.py submit [([(g <group-id>)] <contest-id> <problem-id>)] [<filename>]

Options:
  -v --version  Show version.
  -h --help     Show this screen.
"""
from docopt import docopt

import cmd

if __name__ == '__main__':
    arguments = docopt(__doc__, version="Developer pre-alpha-0.0.1")
    cmd.parse_args(arguments)
