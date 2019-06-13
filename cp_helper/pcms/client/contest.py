from typing import List

import bs4

from cp_helper.pcms.client.core import Client
from cp_helper.pcms.client.login import check_login
from cp_helper.pcms.config.core import Config
from cp_helper.pcms.config.lang import Lang, find_languages
from cp_helper.utils import color


class Contest:
    def __init__(self, id: str = '', url: str = '', client_name: str = ''):
        self.id = id
        self.url = url  # url to switch to that contest
        self.problems = []
        self.client = client_name

    def __str__(self):
        self.switch()
        status, virt = get_contest_status(self.client)
        status_color = 'red'
        if 'RUNNING' in status:
            status_color = 'green'
        elif 'OVER' in status:
            status_color = 'yellow'
        elif "BEFORE" in status:
            status_color = 'blue'

        if virt:
            status = status.rstrip() + ' (Virtual)'
        return self.id + ' ... ' + color(status, fg=status_color, bright_fg=True)

    def __eq__(self, other):
        return self.id == other.id

    def switch(self) -> None:
        if not self.url:
            return
        cl = Client(self.client)
        session = cl.session
        cfg = Config(self.client)
        resp = session.get(cfg.url + 'party/information.xhtml')
        if resp.status_code != 200 and resp.status_code != 302:
            print(color(f'Network Error. Status code:{resp.status_code}', fg='red', bright_fg=True))

        if not check_login(resp.text):
            print(color(f'Not logged. Relogging as {cfg.username}', fg='cyan', bright_fg=True))
            cfg.login()
            cl = Client(self.client)
            session = cl.session

        url = cfg.url + self.url[self.url.index('party'):]
        resp = session.get(url)
        if resp.status_code != 200 and resp.status_code != 302:
            print(color(f'Network Error. Status code:{resp.status_code}', fg='red', bright_fg=True))


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
        cl = Client(name)
        session = cl.session

    resp = session.get(cfg.url + 'party/contests.xhtml')
    if resp.status_code != 200 and resp.status_code != 302:
        print(color(f'Network Error. Status code: {resp.status_code}', fg='red', bright_fg=True))
        return []

    soup = bs4.BeautifulSoup(resp.text, 'html.parser')

    contest_list: bs4.Tag = soup.find('div', {'class': "template-padded"})
    if contest_list is None or resp.url != cfg.url + 'party/contests.xhtml':
        print(color(f"Can't find any contests!", fg='red', bright_fg=True))
        return []
    return [Contest(par.text, par.a['href'] if par.a else '', name) for par in contest_list.find_all('p')]


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
        cl = Client(name)
        session = cl.session
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
        cl = Client(name)
        session = cl.session

    status, _ = get_contest_status(name)

    if status.split(',')[0] != 'RUNNING':
        return []

    resp = session.get(cfg.url + 'party/submit.xhtml')

    return find_languages(resp.text)
