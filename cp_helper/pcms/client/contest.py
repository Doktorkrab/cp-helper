from typing import List

import bs4

from cp_helper.pcms.client.core import Client
from cp_helper.pcms.client.login import check_login
from cp_helper.pcms.config.core import Config
from cp_helper.pcms.config.lang import Lang, find_languages
from cp_helper.utils import color


class Problem:
    def __init__(self, id: str = '', name: str = ''):
        self.id = id
        self.name = name


class Contest:
    def __init__(self, id: str = '', url: str = '', client: Client = None):
        self.id = id
        self.url = url  # url to switch to that contest
        self.problems: List[Problem] = []
        self.client = client

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
            self.client.current_contest = self
            return
        session = self.client.session
        cfg = Config(self.client.name)
        resp = session.get(cfg.url + '/party/information.xhtml')
        if resp.status_code != 200 and resp.status_code != 302:
            print(color(f'Network Error. Status code:{resp.status_code}', fg='red', bright_fg=True))

        if not check_login(resp.text):
            print(color(f'Not logged. Relogging as {cfg.username}', fg='cyan', bright_fg=True))
            cfg.login()
            self.client.load()
            session = self.client.session

        url = cfg.url + '/' + self.url[self.url.index('party'):]
        resp = session.get(url)
        if resp.status_code != 200 and resp.status_code != 302:
            print(color(f'Network Error. Status code:{resp.status_code}', fg='red', bright_fg=True))

        self.client.current_contest = self
        self.client.save()


def get_contests_list(cl: Client) -> List[Contest]:
    session = cl.session
    cfg = Config(cl.name)
    resp = session.get(cfg.url + '/party/information.xhtml')
    if resp.status_code != 200 and resp.status_code != 302:
        print(color(f'Network Error. Status code:{resp.status_code}', fg='red', bright_fg=True))
        return []

    if not check_login(resp.text):
        print(color(f'Not logged. Relogging as {cfg.username}', fg='cyan', bright_fg=True))
        cfg.login()
        cl.load()
        session = cl.session

    resp = session.get(cfg.url + '/party/contests.xhtml')
    if resp.status_code != 200 and resp.status_code != 302:
        print(color(f'Network Error. Status code: {resp.status_code}', fg='red', bright_fg=True))
        return []

    soup = bs4.BeautifulSoup(resp.text, 'html.parser')

    contest_list: bs4.Tag = soup.find('div', {'class': "template-padded"})
    if contest_list is None or resp.url != cfg.url + '/party/contests.xhtml':
        print(color(f"Can't find any contests!", fg='red', bright_fg=True))
        return []
    for par in contest_list.find_all('p'):
        if not par.a:
            cl.current_contest = Contest(par.text, '', cl)
            cl.current_contest.switch()
            cl.save()
            break
    ret = [Contest(par.text, par.a['href'] if par.a else '', cl) for par in contest_list.find_all('p')]
    can_switch: List[Contest] = list(filter(lambda x: x.url != '', ret))
    lst = cl.current_contest
    if len(can_switch) > 0:
        can_switch[0].switch()
        resp = session.get(cfg.url + '/party/contests.xhtml')
        soup = bs4.BeautifulSoup(resp.text, 'html.parser')

        contest_list1 = list(soup.find('div', {'class': "template-padded"}).find_all('p'))
        for i in range(len(contest_list1)):
            ret[i] = ret[i] if ret[i].url != '' else Contest(contest_list1[i].text, contest_list1[i].a['href'], cl)
            if lst == ret[i]:
                cl.current_contest = ret[i]
    return ret


def get_contest_status(cl: Client) -> [str, bool]:
    session = cl.session
    cfg = Config(cl.name)
    resp = session.get(cfg.url + '/party/information.xhtml')
    if resp.status_code != 200 and resp.status_code != 302:
        print(color(f'Network Error. Status code:{resp.status_code}', fg='red', bright_fg=True))
        return 'UNKNOWN, 0:00 of 0:00'

    if not check_login(resp.text):
        print(color(f'Not logged. Relogging as {cfg.username}', fg='cyan', bright_fg=True))
        cfg.login()
        cl.load()
        session = cl.session
        resp = session.get(cfg.url + '/party/information.xhtml')

    soup = bs4.BeautifulSoup(resp.text, 'html.parser')
    clock = soup.find('span', id='running-clock')
    if clock is None:
        return 'UNKNOWN, 0:00 of 0:00'
    return clock.text.splitlines()[0], 'Virtual Contest' in resp.text


def get_contest_langs(cl: Client) -> List[Lang]:
    session = cl.session
    cfg = Config(cl.name)
    resp = session.get(cfg.url + '/party/information.xhtml')
    if resp.status_code != 200 and resp.status_code != 302:
        print(color(f'Network Error. Status code:{resp.status_code}', fg='red', bright_fg=True))
        return []

    if not check_login(resp.text):
        print(color(f'Not logged. Relogging as {cfg.username}', fg='cyan', bright_fg=True))
        cfg.login()
        cl = Client(cl.name)
        session = cl.session

    status, _ = get_contest_status(cl)

    if status.split(',')[0] != 'RUNNING':
        return []

    resp = session.get(cfg.url + '/party/submit.xhtml')

    return find_languages(resp.text)
