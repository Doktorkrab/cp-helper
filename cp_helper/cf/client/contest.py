import re
from os import makedirs, chdir

from cp_helper.cf.config import Config
from cp_helper.utils import choose_yn, pretty_test_num, color
from .core import Client
from .login import check_login


class Problem(object):
    def __init__(self, problem_id: str = '', url: str = ''):
        self.id = problem_id
        cfg = Config()
        self.url = 'https://codeforces.com' + url + f'?locale={cfg.lang}'
        self.samples_in = []
        self.samples_out = []

    def parse(self):
        self.samples_in, self.samples_out = parse_problem(self)
        if len(self.samples_in) != len(self.samples_out):
            print(color('Error occurred while problem was parsing', fg='Red', bright_fg=True))
            self.samples_in, self.samples_out = [], []

    def save(self):
        for num, inp in enumerate(self.samples_in):
            pretty_num = pretty_test_num(num + 1, len(self.samples_in) - 1)
            with open(f'{pretty_num}', 'w') as sample:
                print(inp.strip().rstrip(), file=sample)
        for num, out in enumerate(self.samples_out):
            pretty_num = pretty_test_num(num + 1, len(self.samples_out) - 1)
            with open(f'{pretty_num}.a', 'w') as sample:
                print(out.strip().rstrip(), file=sample)


class Contest(object):
    def __init__(self, contest_id: str, group):
        self.id = contest_id
        self.group = group if group else ''
        block = find_problems_block(self)
        self.problems = find_problems(block)

    def parse(self):
        print(color(f'Found {len(self.problems)} problems', fg='blue', bright_fg=True))
        for problem in self.problems:
            problem.parse()
            print(color(f'Parsed {problem.id} with {len(problem.samples_in)} samples', fg='green', bright_fg=True))

    def create_directories(self):
        folder_name = self.id
        if self.group:
            folder_name += f'_{self.group}'

        for problem in self.problems:
            try:
                makedirs(f'{folder_name}/{problem.id}')
            except FileExistsError:
                if not choose_yn(f'Directory for {self.id}{f"(from group {self.group})" if self.group else ""}'
                                 + f"'s problem {problem.id} already exists. Rewrite?"):
                    continue
            chdir(f'{folder_name}/{problem.id}')
            problem.save()
            chdir('../..')

    def get_url(self):
        return f"https://codeforces.com{'/group/' + self.group if self.group else ''}/contest/{self.id}"


def find_problems_block(contest: Contest):
    session = Client().get_session()
    cfg = Config()

    url = contest.get_url()
    resp = session.get(url)

    if not check_login(resp.text, cfg.username):
        cfg.login()
        session = Client().get_session()
        resp = session.get(url)
    tmp = re.findall(r'class="problems">([\S\s]*?)</table>', resp.text)

    if len(tmp) == 0:
        print(color("Can't found any problems!", fg='red', bright_fg=True))
        return
    if len(tmp) != 1:
        print(color('Multiple problems block!', fg='red', bright_fg=True))
        return
    return tmp[0]


def find_problems(problems_block: str):
    parsed = re.findall(r'class="id">\s*?<a href="([\S\s]+?)">[\s]*([\S ]+?)[\s]*?</a>', problems_block)
    return [Problem(y, x) for x, y in parsed]


def parse_problem(problem: Problem):
    session = Client().get_session()
    resp = session.get(problem.url)
    if resp.url != problem.url:
        print(color("No problem statements with chosen language.", fg='red', bright_fg=True))
        return [], []
    text = resp.text.replace('<br />', '\n')
    input_samples = re.findall(r'class="input">[\S\s]+?<pre>([\s\S]+?)</pre>', text)
    output_samples = re.findall(r'class="output">[\S\s]+?<pre>([\s\S]+?)</pre>', text)
    return input_samples, output_samples
