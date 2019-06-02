#! /usr/bin/env python3
"""
cp-helper - Competitive programming tool. You should run "cp-helper config user" and "cp-helper config template add"

Usage:
  cp-helper (-v|--version)
  cp-helper (-h|--help)
  cp-helper config user
  cp-helper config template (add|delete|default)
  cp-helper config lang
  cp-helper config
  cp-helper fetch [(g <group-id>)] [<contest-id>] [<problem-id>]
  cp-helper test [<filename>]
  cp-helper submit [([(g <group-id>)] <contest-id> <problem-id>)] [<filename>]
  cp-helper open [(g <group-id>)] [<contest-id>] [<problem-id>]

Options:
  -v --version  Show version.
  -h --help     Show this screen.

Examples:
    cp-helper config user - config your username and password
    cp-helper config template add - add a new template
    cp-helper config template delete - delete a existed template
    cp-helper config template default - set default template(doesn't matter now)
    cp-helper config lang - set locale for codeforces problem name
    cp-helper config - print config
    cp-helper fetch g hehhHdJ2Yg 245388 A - fetch problem A from contest 245388 from group hehhHdJ2Yg(group id, not name)
    cp-helper fetch g hehhHdJ2Yg 245388 - fetch contest 245388 from group hehhHdJ2Yg(group id, not name, copy from url)
    cp-helper fetch 1148 A - fetch problem A from contest 1148(contest id, copy from url)
    cp-helper fetch 1148 - fetch contest 1148
    cp-helper fetch - fetch current problem from current contest(your path must be like 'contest-id(_group_id)/problem-id')
    cp-helper test code.cpp - run code.cpp on all samples from current problem
    cp-helper test - find code file and test on all samples from current problem
    cp-helper submit - find code file and submit. You can manually specify contest-id/group-id/filename
    cp-helper open - open a contest/problem page in your default browser
"""
from docopt import docopt

import cmd

if __name__ == '__main__':
    arguments = docopt(__doc__, version="Developer pre-alpha-0.0.1")
    cmd.parse_args(arguments)
