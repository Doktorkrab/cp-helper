from client.contest import Contest


def parse_fetch(args: dict) -> None:
    contest = Contest(args['<contest_id>'], args['<group_id>'])
    contest.parse()
    contest.create_directories()
