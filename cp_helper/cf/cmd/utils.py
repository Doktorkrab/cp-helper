from os import listdir
from os.path import abspath, basename, splitext, isfile
from typing import Optional, Tuple

from cp_helper.cf.config.core import CodeTemplate, Config
from cp_helper.utils import color


def get_contest_id(args: dict) -> Optional[str]:
    if args['<contest-id>']:
        contest_id = args['<contest-id>']
    else:
        contest_id = basename(abspath('../')).split('_')[0]
    if not contest_id.isdigit():
        print(color("Contest id not a number or can't find valid contest id", fg='Red', bright_fg=True))
        return None
    return contest_id


def get_problem_id(args: dict) -> str:
    if args['<problem-id>']:
        problem_id = args['<problem-id>']
    else:
        problem_id = basename(abspath('./'))
    return problem_id.upper()


def get_group_id(args: dict) -> Optional[str]:
    if args['<group-id>']:
        group_id = args['<group-id>']
    else:
        group_id = basename(abspath('../')).split('_')
        if len(group_id) < 2:
            group_id = ''
        else:
            group_id = group_id[1]
    return group_id


def find_code(args: dict) -> Optional[Tuple[str, CodeTemplate]]:
    suitable_pairs = []
    cfg = Config()
    if not len(cfg.templates):
        print(color('Please add template with ./cp-helper config template add', fg='Yellow', bright_fg=True))
        return None
    if args['<filename>']:
        _, ext = splitext(args['<filename>'])
        ext = ext[1:]
        for template in cfg.templates:
            if template.lang.suffix == ext:
                suitable_pairs.append((args['filename'], template))

    for file in listdir('.'):
        if not isfile(file):
            continue

        _, ext = splitext(file)
        ext = ext[1:]
        for template in cfg.templates:
            if template.lang.suffix == ext:
                suitable_pairs.append((file, template))

    if len(suitable_pairs) == 0:
        print(color("Can't find any valid file.", fg='Red', bright_fg=True))
        return None
    if len(suitable_pairs) == 1:
        return suitable_pairs[0]
    for num, pair in enumerate(suitable_pairs):
        file, template = pair
        print(f'#{num + 1}|File:{file}')
        print(f'{" " * (len(str(num + 1)) + 1)}|Template:{template}')
    ind = input('Please, choose one: ')
    while not (ind.isdigit() and 0 <= int(ind) - 1 < len(suitable_pairs)):
        ind = input('Please, choose one: ')
    return suitable_pairs[int(ind) - 1]
