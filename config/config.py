import json
import marshal

from . import CONFIG_PATH


class Config(object):
    def __init__(self):
        self.username: str = ''
        self.password: str = ''
        self.templates = []
        self.default_template = -1
        self.load()

    def __repr__(self):
        return f"Config('{self.username}', '{self.password}', {self.templates}, {self.default_template})"

    def __str__(self):
        return f'Codeforces account username: {self.username}\nCodeforces account password(encrypted): ' + \
               f'{self.password}\nCurrent templates: {self.templates}\n' + \
               f'Default template: {"None" if self.default_template == -1 else self.templates[self.default_template]}'

    def save(self):
        try:
            with open(CONFIG_PATH, 'wb') as config_file:
                marshal.dump(json.dumps(self, cls=ConfigEncoder), config_file)
        except Exception as e:
            print("[ERROR!] Didn't saved! Exception:", e)

    def load(self):
        try:
            with open(CONFIG_PATH, 'rb') as config_file:
                dct = json.loads(marshal.load(config_file))
                self.username = dct['username']
                self.password = dct['password']
                self.templates = dct['templates']
                self.default_template = dct['default_template']
        except FileNotFoundError:
            pass


class ConfigEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Config):
            return o.__dict__
        else:
            return super().default(o)
