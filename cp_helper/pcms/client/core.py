import pickle

from requests import Session


class Client(object):
    def __init__(self, path: str):
        self.username = ''
        self.path = path
        self.cookies = None
        self.load()

    def save(self):
        with open(self.path, 'wb') as session_file:
            pickle.dump(self.username, session_file)
            pickle.dump(self.cookies, session_file)

    def load(self):
        try:
            with open(self.path, 'rb') as session_file:
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
