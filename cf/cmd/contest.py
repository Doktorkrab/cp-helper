from webbrowser import open_new_tab

from cf.client.contest import Contest
from cf.client.submission import submit
from utils import color
from .utils import get_contest_id, get_group_id, get_problem_id, find_code


def parse_fetch(args: dict) -> None:
    contest_id, group_id = get_contest_id(args), get_group_id(args)
    if contest_id is None:
        return
    contest = Contest(contest_id, group_id)
    contest.parse()
    problem_id = get_problem_id(args)
    for problem in contest.problems:
        if problem.id == problem_id:
            problem.save()
    contest.create_directories()


def parse_submit(args: dict):
    contest_id, group_id = get_contest_id(args), get_group_id(args)
    if contest_id is None:
        return
    contest = Contest(contest_id, group_id)
    ret = find_code(args)
    if ret is None:
        print(color("""Can't find any code file.
        Please add template by "cp-helper config template add"
        'Or choose file manually'""", fg='Red', bright_fg=True))
        return
    code, template = ret
    submit(contest, get_problem_id(args), code, template)


def parse_open(args: dict):
    contest_id, group_id = get_contest_id(args), get_group_id(args)
    if contest_id is None:
        return
    problem_id = get_problem_id(args)
    if problem_id is None:
        open_new_tab(Contest(contest_id, group_id).get_url())
    else:
        contest = Contest(contest_id, group_id)
        for i in contest.problems:
            if i.id == problem_id:
                open_new_tab(i.url)
                break
        else:
            print(color(f'No problem {problem_id} in contest {contest_id}', fg='red', bright_fg=True))
