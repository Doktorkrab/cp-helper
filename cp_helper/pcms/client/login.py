from bs4 import BeautifulSoup

from cp_helper.pcms.client.core import Client
from cp_helper.utils import color


def check_login(body: str) -> bool:
    soup = BeautifulSoup(body, 'html.parser')
    return soup.find('td', text='Login name') is not None


def login(username: str, password: str, name: str, url: str) -> None:
    cl = Client(name)
    session = cl.session

    login_url = url + 'login.xhtml'
    resp = session.get(login_url)

    if resp.status_code != 200 and resp.status_code != 302:
        print(login_url)
        print(color(f'Network error at get! Status code: {resp.status_code}', fg='red', bright_fg=True))
        return

    print(f'Logging in as {username}')
    resp = session.post(login_url, data={
        'login': 'login',
        "login:name": username,
        "login:password": password,
        'login:login': '',
        'javax.faces.ViewState': 'stateless',
    })

    if resp.status_code != 200 and resp.status_code != 302:
        print(color(f'Network error at post! Status code{resp.status_code}', fg='red', bright_fg=True))
        return

    resp = session.post(url + 'set-locale.xhtml', data={
        'locale-name': "English",
        'return-path': '/party/information.xhtml?'
    })
    if resp.status_code != 200 and resp.status_code != 302:
        print(color(f'Network error at set-locale! Status code{resp.status_code}', fg='red', bright_fg=True))
        return

    if not check_login(resp.text):
        print(color(f'Invalid user/password', fg='red', bright_fg=True))
        return

    print(color(f'Logged in as {username}', fg='green', bright_fg=True))

    cl.username = username
    cl.cookies = session.cookies
    cl.save()
