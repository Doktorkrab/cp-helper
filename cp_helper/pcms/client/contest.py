from typing import List

import bs4

from cp_helper.pcms.client.core import Client
from cp_helper.pcms.client.login import check_login
from cp_helper.pcms.config.core import Config
from cp_helper.pcms.config.lang import Lang, find_languages
from cp_helper.utils import color


class Contest:
    def __init__(self, id: str = '', url: str = ''):
        self.id = id
        self.url = url  # url to switch to that contest
        self.problems = []

    def __str__(self):
        return f'{self.id}(url: {self.url}, problems: {len(self.problems)})'

    def __eq__(self, other):
        return self.id == other.id


def get_contests_list(name: str) -> List[Contest]:
    cl = Client(name)
    session = cl.session
    cfg = Config(name)
    resp = session.get(cfg.url + 'party/information.xhtml')
    if resp.status_code != 200 and resp.status_code != 302:
        print(color(f'Network Error. Status code:{resp.status_code}', fg='red', bright_fg=True))
        return []

    if not check_login(resp.text):
        print(color(f'Not logged. Relogging as {cfg.username}', fg='cyan', bright_fg=True))
        cfg.login()

    resp = session.get(cfg.url + 'party/contests.xhtml')
    if resp.status_code != 200 and resp.status_code != 302:
        print(color(f'Network Error. Status code: {resp.status_code}', fg='red', bright_fg=True))
        return []

    soup = bs4.BeautifulSoup(resp.text, 'html.parser')

    contest_list: bs4.Tag = soup.find('div', {'class': "template-padded"})
    if contest_list is None or resp.url != cfg.url + 'party/contests.xhtml':
        print(color(f"Can't find any contests!", fg='red', bright_fg=True))
        return []
    return [Contest(par.text, par.a['href'] if par.a else '') for par in contest_list.find_all('p')]


def get_contest_status(name: str) -> [str, bool]:
    cl = Client(name)
    session = cl.session
    cfg = Config(name)
    resp = session.get(cfg.url + 'party/information.xhtml')
    if resp.status_code != 200 and resp.status_code != 302:
        print(color(f'Network Error. Status code:{resp.status_code}', fg='red', bright_fg=True))
        return 'UNKNOWN, 0:00 of 0:00'

    if not check_login(resp.text):
        print(color(f'Not logged. Relogging as {cfg.username}', fg='cyan', bright_fg=True))
        cfg.login()
        resp = session.get(cfg.url + 'party/information.xhtml')

    soup = bs4.BeautifulSoup(resp.text, 'html.parser')
    clock = soup.find('span', id='running-clock')
    if clock is None:
        return 'UNKNOWN, 0:00 of 0:00'
    return clock.text.splitlines()[0], 'Virtual Contest' in resp.text


def get_contest_langs(name: str) -> List[Lang]:
    cl = Client(name)
    session = cl.session
    cfg = Config(name)
    resp = session.get(cfg.url + 'party/information.xhtml')
    if resp.status_code != 200 and resp.status_code != 302:
        print(color(f'Network Error. Status code:{resp.status_code}', fg='red', bright_fg=True))
        return []

    if not check_login(resp.text):
        print(color(f'Not logged. Relogging as {cfg.username}', fg='cyan', bright_fg=True))
        cfg.login()

    status, _ = get_contest_status(name)

    if status.split(',')[0] != 'RUNNING':
        return []

    resp = session.get(cfg.url + 'party/submit.xhtml')

    return find_languages(resp.text)
