import re

from utils import color
from .client import Client


def regexp_wrapper(regexp: str, body: str) -> str:
    found = re.findall(regexp, body)
    if len(found) == 0:
        # TODO: Make it better
        raise Exception
    return found[0]


def get_csrf_token(body: str) -> str:
    return regexp_wrapper("name='csrf_token' value='(.+?)'/>", body)


def get_ftaa(body: str) -> str:
    tmp = regexp_wrapper('window._ftaa = "(.+)";', body)
    if tmp == 'n/a':
        tmp = ''
    return tmp


def get_bfaa(body: str) -> str:
    tmp = regexp_wrapper('window._bfaa = "(.+)";', body)
    if tmp == 'n/a':
        tmp = ''
    return tmp


def check_login(body: str, username: str) -> bool:
    return len(re.findall(f'handle = "{username}"', body)) != 0


def login(username: str, password: str):
    client = Client()
    session = client.get_session()

    resp = session.get('https://codeforces.com/enter')

    csrf = get_csrf_token(resp.text)
    ftaa = get_ftaa(resp.text)
    bfaa = get_bfaa(resp.text)

    resp = session.post('https://codeforces.com/enter', data={
        'csrf_token': csrf,
        'action': 'enter',
        'ftaa': ftaa,
        'bfaa': bfaa,
        'handleOrEmail': username,
        'password': password,
        '_tta': 176
    })
    if resp.status_code != 302 and resp.status_code != 200:
        raise Exception

    resp = session.get('https://codeforces.com/')
    if not check_login(resp.text, username):
        # TODO: Make it better
        raise Exception

    print(color('Login succeed!', fg='green', bright_fg=True))
    client.username = username
    client.ftaa = ftaa
    client.bfaa = bfaa
    client.cookies = session.cookies
    client.save()
