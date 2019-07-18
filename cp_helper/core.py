#! /usr/bin/env python3
"""
cp-helper - Competitive programming tool. You should run "cp-helper config user" and "cp-helper config template add"

Usage:
  cp-helper cf (-v|--version)
  cp-helper cf (-h|--help)
  cp-helper cf config user
  cp-helper cf config template (add|delete|default)
  cp-helper cf config lang
  cp-helper cf config
  cp-helper cf fetch [(g <group-id>)] [<contest-id>] [<problem-id>]
  cp-helper cf test [<filename>]
  cp-helper cf submit [([(g <group-id>)] <contest-id> <problem-id>)] [<filename>]
  cp-helper cf open [(g <group-id>)] [<contest-id>] [<problem-id>]
  cp-helper pcms config print [<config-name>]
  cp-helper pcms config new <config-name>
  cp-helper pcms config <config-name> template add
  cp-helper pcms config <config-name> template delete
  cp-helper pcms config <config-name> update
  cp-helper pcms config <config-name> switch

Options:
  -v --version  Show version.
  -h --help     Show this screen.

Examples:
    cp-helper cf config user - config your username and password
    cp-helper cf config template add - add a new template
    cp-helper cf config template delete - delete a existed template
    cp-helper cf config template default - set default template(doesn't matter now)
    cp-helper cf config lang - set locale for codeforces problem name
    cp-helper cf config - print config
    cp-helper cf fetch g hehhHdJ2Yg 245388 A - fetch problem A from contest 245388 from group hehhHdJ2Yg(group id, not name)
    cp-helper cf fetch g hehhHdJ2Yg 245388 - fetch contest 245388 from group hehhHdJ2Yg(group id, not name, copy from url)
    cp-helper cf fetch 1148 A - fetch problem A from contest 1148(contest id, copy from url)
    cp-helper cf fetch 1148 - fetch contest 1148
    cp-helper cf fetch - fetch current problem from current contest(your path must be like 'contest-id(_group_id)/problem-id')
    cp-helper cf test code.cpp - run code.cpp on all samples from current problem
    cp-helper cf test - find code file and test on all samples from current problem
    cp-helper cf submit - find code file and submit. You can manually specify contest-id/group-id/filename
    cp-helper cf open - open a contest/problem page in your default browser
"""
from docopt import docopt

import cp_helper.cf.cmd
import cp_helper.pcms.cmd


def parse():
    arguments = docopt(__doc__, version="Alpha 1(codeforces edition)")
    if arguments['cf']:
        cp_helper.cf.cmd.parse_args(arguments)
    elif arguments['pcms']:
        cp_helper.pcms.cmd.parse_args(arguments)


if __name__ == "__main__":
    parse()
