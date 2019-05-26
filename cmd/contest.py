from client.contest import Contest
from .utils import get_contest_id, get_group_id, get_problem_id


def parse_fetch(args: dict) -> None:
    contest = Contest(get_contest_id(args), get_group_id(args))
    contest.parse()
    problem_id = get_problem_id(args)
    for problem in contest.problems:
        if problem.id == problem_id:
            problem.save()
    contest.create_directories()
