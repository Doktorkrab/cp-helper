import pickle

from requests import Session

from cp_helper.cf.config import SESSION_PATH


class Client(object):
    def __init__(self):
        self.username: str = ''
        self.ftaa: str = ''
        self.bfaa: str = ''
        self.cookies = None
        self.load()

    def save(self):
        with open(SESSION_PATH, 'wb') as session_file:
            pickle.dump(self.username, session_file)
            pickle.dump(self.ftaa, session_file)
            pickle.dump(self.bfaa, session_file)
            pickle.dump(self.cookies, session_file)

    def load(self):
        try:
            with open(SESSION_PATH, 'rb') as session_file:
                self.username = pickle.load(session_file)
                self.ftaa = pickle.load(session_file)
                self.bfaa = pickle.load(session_file)
                self.cookies = pickle.load(session_file)
        except FileNotFoundError:
            pass

    def get_session(self) -> Session:
        s = Session()
        if self.cookies is not None:
            s.cookies = self.cookies
        return s
