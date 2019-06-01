from datetime import datetime
from platform import system
from re import findall
from subprocess import call
from time import sleep, time
from typing import List
import bs4

from config.config import CodeTemplate, Config
from .client import Client
from .contest import Contest
from .login import get_csrf_token, check_login
from utils import color

VERDICTS = {"RUNTIME_ERROR": "RE",
            "WRONG_ANSWER": "WA",
            "TIME_LIMIT_EXCEEDED": "TLE",
            "MEMORY_LIMIT_EXCEEDED": "MLE",
            "IDLENESS_LIMIT_EXCEEDED": "ILE",
            "OK": "OK",
            "COMPILATION_ERROR": "CE",
            "TESTING": "Testing",
            "WAITING": "Waiting",
            "UNKNOWN": "Unknown",
            "PARTIAL": "Relative Scoring"}


class Submisson(object):
    def __init__(self, tag: bs4.element.Tag):
        self.id: int = int(tag.find('td', {'class': 'id-cell'}).text)
        self.author: str = tag.find('td', {'class': 'status-party-cell'}).text.strip().rstrip()
        parameters = tag.find_all('td', {'class': 'status-small'})
        self.date: datetime = datetime.strptime(parameters[0].text.strip().rstrip(), '%d.%m.%Y %H:%M')
        self.problem: str = parameters[1].text.strip().rstrip()
        if tag is not None and tag.find('td', {'class': 'time-consumed-cell'}) is not None:
            self.time: str = tag.find('td', {'class': 'time-consumed-cell'}).text.strip().rstrip()
        else:
            self.time: str = ''
        if tag is not None and tag.find('td', {'class': 'memory-consumed-cell'}) is not None:
            self.memory: str = tag.find('td', {'class': 'memory-consumed-cell'}).text.strip().rstrip()
        else:
            self.memory: str = ''

        tmp = tag.find('td', {'class': 'status-cell'})
        self.status: str = 'WAITING' if tmp is None or tmp.span is None else tmp.span['submissionverdict']
        if tmp.span is None and tmp['waiting'] == 'false':
            self.status = 'UNKNOWN'
        self.test: int = -1 if tmp is None or \
                               tmp.find('span', {'class': 'verdict-format-judged'}) is None else \
            int(tmp.find('span', {'class': 'verdict-format-judged'}).text)

    def __str__(self):
        ret = ''
        ret += f'Submission: #{self.id}\n'
        ret += f'Author: {self.author}\n'
        ret += f'Date: {self.date.strftime("%d.%m.%Y %H:%M")}\n'
        ret += f'Problem: {self.problem}\n'
        ret += f'Status: {VERDICTS[self.status]}' + ('\n' if self.test == -1 else f' #{self.test}\n')
        ret += f'Time: {self.time}\n' if self.time else ''
        ret += f'Memory: {self.memory}' if self.time else ''
        return ret.rstrip()


def find_error(body: str) -> str:
    found = findall(r'''for__source['"]>([\s\S]+?)</''', body)
    if len(found) != 0:
        return '/'.join(found)
    else:
        return 'Unknown error!'


def submit(contest: Contest, problem_id: str, source_code: str, template: CodeTemplate) -> None:
    if contest is None or problem_id is None:
        print(color("Can't find contest by this id or can't find problem by this problem id", fg='red', bright_fg=True))
        return

    client = Client()
    session = client.get_session()
    cfg = Config()
    submit_url = contest.get_url() + '/submit'
    my_url = contest.get_url() + '/my'

    resp = session.get(submit_url)

    if not check_login(resp.text, client.username):
        cfg.login()
        resp = session.get(submit_url)
    csrf = get_csrf_token(resp.text)
    with open(source_code) as f:
        code = f.read()

    print(color(f"Submiting in contest {contest.id} problem {problem_id}.", fg='blue', bright_fg=True))
    resp = session.post(submit_url, data={
        "csrf_token": csrf,
        "ftaa": client.ftaa,
        "bfaa": client.bfaa,
        "action": "submitSolutionFormSubmitted",
        "programTypeId": template.lang.id,
        "submittedProblemIndex": problem_id,
        "source": code,
        "tabSize": 4,
        "_tta": 594,
        "sourceCodeConfirmed": True
    })

    if resp.url == my_url:
        print(color('Submitted successfully!', fg='green', bright_fg=True))
    else:
        print(color(f'{find_error(resp.text)}', fg='red', bright_fg=True))
    watch_submission(contest)


def get_submissions(contest: Contest, n: int = 1, all_submissions: bool = False) -> List[Submisson]:
    cfg = Config()
    client = Client()
    session = client.get_session()
    url = contest.get_url() + '/my' if not all_submissions else '/status'

    resp = session.get(url)

    if not check_login(resp.text, client.username):
        cfg.login()
        resp = session.get(url)

    parsed_html = bs4.BeautifulSoup(resp.text, 'html.parser')

    table: bs4.element.Tag = parsed_html.find_all('table', {'class': "status-frame-datatable"})[0]
    submissions = []
    for row in table.find_all('tr')[1:]:
        submissions.append(Submisson(row))
        if len(submissions) == n:
            return submissions


def watch_submission(contest: Contest):
    if system() == 'Windows':  # Make ansi work in Windows
        call('', shell=True)
    sub = None
    flag = False
    while sub is None or sub.status == 'WAITING' or sub.status == 'TESTING':
        start = time()
        if flag:
            for i in range(len(str(sub).splitlines())):
                print(u'\u001b[A\u001b[2K', end='')
        sub = get_submissions(contest)[0]
        flag = True
        print(sub)
        diff = time() - start
        if diff < 1:
            sleep(1 - diff)
