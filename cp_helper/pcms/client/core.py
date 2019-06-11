import pickle
from os import makedirs

from requests import Session

from cp_helper.pcms.config import CONFIG_PATH


class Client(object):
    def __init__(self, name: str):
        self.username = ''
        self.name = name
        self.cookies = None
        self.load()

    def save(self):
        makedirs(f'{CONFIG_PATH}/{self.name}', exist_ok=True)
        with open(f'{CONFIG_PATH}/{self.name}/session', 'wb') as session_file:
            pickle.dump(self.username, session_file)
            pickle.dump(self.cookies, session_file)

    def load(self):
        try:
            with open(f'{CONFIG_PATH}/{self.name}/session', 'rb') as session_file:
                self.username = pickle.load(session_file)
                self.cookies = pickle.load(session_file)
        except FileNotFoundError:
            pass

    @property
    def session(self) -> Session:
        s = Session()
        if self.cookies is not None:
            s.cookies = self.cookies
        return s
