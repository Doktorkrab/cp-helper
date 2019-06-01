from client.contest import Contest
from client.submission import submit
from .utils import get_contest_id, get_group_id, get_problem_id, find_code
from utils import color


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
