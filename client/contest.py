import re

from config import Config
from .client import Client


class Problem(object):
    def __init__(self, problem_id: str = '', url: str = ''):
        self.id = problem_id
        self.url = url
        self.samples_in = []
        self.samples_out = []

    def parse(self):
        self.samples_in, self.samples_out = parse_problem(self)
        if len(self.samples_in) != len(self.samples_out):
            print('Error occurred while problem was parsing')
            self.samples_in, self.samples_out = [], []


class Contest(object):
    def __init__(self, contest_id: str, group: str = ''):
        self.id = contest_id
        self.group = group
        self.problems = []

    def parse(self):
        block = find_problems_block(self)
        self.problems = find_problems(block)
        print(f'Found {len(self.problems)} problems')
        for problem in self.problems:
            problem.parse()
            print(f'Parsed {problem.id} with {len(problem.samples_in)}')


def find_problems_block(contest: Contest):
    session = Client().get_session()
    url = f"https://codeforces.com{'/group/' + contest.group if contest.group else ''}/contest/{contest.id}"

    resp = session.get(url)
    tmp = re.findall(r'class="problems">([\S\s]*?)</table>', resp.text)

    if len(tmp) == 0:
        print("Can't found any problems!")
        return
    if len(tmp) != 1:
        print('Multiple problems block!')
        return
    return tmp[0]


def find_problems(problems_block: str):
    parsed = re.findall(r'class="id">\s*?<a href="([\S\s]+?)">[\s]*([\S ]+?)[\s]*?</a>', problems_block)
    return [Problem(y, x) for x, y in parsed]


def parse_problem(problem: Problem):
    url = 'https://codeforces.com' + problem.url + '?locale=ru'
    session = Client().get_session()
    cfg = Config()
    resp = session.get(url)
    text = resp.text.replace('<br />', '\n')
    input_samples = re.findall(r'class="input">[\S\s]+?<pre>([\s\S]+?)</pre>', text)
    output_samples = re.findall(r'class="output">[\S\s]+?<pre>([\s\S]+?)</pre>', text)
    return input_samples, output_samples
