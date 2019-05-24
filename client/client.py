from requests.cookies import RequestsCookieJar


class Client(object):
    def __init__(self, username: str = '', cookies=None):
        self.username: str = username
        self.ftaa: str = ''
        self.bfaa: str = ''
        self.cookies: RequestsCookieJar = cookies
