import os.path
import pickle
from getpass import getpass
from typing import List

from cf import client
from utils import choose_yn, color
from . import CONFIG_PATH
from .langs import lang_list, Lang


class Config(object):
    def __init__(self):
        self.username: str = ''
        self.password: str = ''
        self.templates: List[CodeTemplate] = []
        self.default_template: int = -1
        self.lang: str = 'ru'
        self.load()

    def __repr__(self):
        return f"Config('{self.username}', '{self.password}', {self.templates}, {self.default_template})"

    def __str__(self):
        ret = f'Codeforces account username: {self.username}\nCodeforces account password(encrypted): ' + \
              f'{self.password}\nCurrent templates: '
        if len(self.templates) == 0:
            ret += '[]\n'
        else:
            ret += '['
            for i in range(len(self.templates)):
                ret += str(self.templates[i])
                ret += ', ' if i != len(self.templates) - 1 else ']\n'
        ret += f'Default template: {"None" if self.default_template == -1 else self.templates[self.default_template]}'
        return ret

    def save(self):
        try:
            with open(CONFIG_PATH, 'wb') as config_file:
                pickle.dump(self.username, config_file)
                pickle.dump(self.password, config_file)
                pickle.dump(self.templates, config_file)
                pickle.dump(self.default_template, config_file)
                pickle.dump(self.lang, config_file)

        except Exception as e:
            print(color("Didn't saved! Exception: " + str(e), fg='Red', bright_fg=True))

    def load(self):
        try:
            with open(CONFIG_PATH, 'rb') as config_file:
                self.username = pickle.load(config_file)
                self.password = pickle.load(config_file)
                self.templates = pickle.load(config_file)
                self.default_template = pickle.load(config_file)
                self.lang = pickle.load(config_file)
        except FileNotFoundError:
            pass

    def add_template(self):
        id_to_index = {}
        for index, lang in enumerate(lang_list):
            print(f'{lang.id}: {lang.name}')
            id_to_index[lang.id] = index

        chosen_id = -1
        while chosen_id == -1:
            chosen = input('Please choose a number(e.g. 54):')
            if not chosen.isdigit() or int(chosen) not in id_to_index:
                print(color('Please choose a valid number', fg='Red', bright_fg=True))
                continue
            chosen_id = int(chosen)

        path = ''
        while len(path) == 0:
            tmp_path = input(
                'Please specify a path to template(e.g. template.cpp, ./template.cpp, ~/template.cpp, empty):')
            tmp_path = os.path.abspath(os.path.expanduser(tmp_path))
            if os.path.exists(tmp_path):
                path = tmp_path
                break
            print(color("Path doesn't exists", fg='Red', bright_fg=True))

        compile_cmd = input('Please specify a compile command(may be empty):')

        run_cmd = input('Please specify a run command(e.g. ./%file%)')
        while len(run_cmd) == 0:
            print(color('Run command cannot be empty', fg='Red', bright_fg=True))
            run_cmd = input('Please specify a run command(e.g. ./%file%)')

        clean_cmd = input('Please specify a command after run(e. g. rm %file%)')

        self.templates.append(CodeTemplate(lang_list[id_to_index[chosen_id]], path, compile_cmd, run_cmd, clean_cmd))

        if choose_yn(color('Set it default now?', fg='blue', bright_fg=True)):
            self.set_default_template(len(self.templates) - 1)
        print(color('Added!', fg='green', bright_fg=True))
        self.save()

    def delete_template(self):
        for index, template in enumerate(self.templates):
            print(f'{index}: {template.path_to}')

        index = input('Please specify the index to delete: ')
        while not (index.isdigit() and 0 <= int(index) < len(self.templates)):
            print(color('Please enter valid index', fg='Red', bright_fg=True))
            index = input('Please specify the index to delete: ')

        index = int(index)
        if not choose_yn(color(f'You want to delete #{index} template. Are you sure?', fg='magenta', bright_fg=True,
                               bold=True, underline=True)):
            return
        if self.default_template != -1 and self.default_template > index:
            self.default_template -= 1
        if self.default_template == index:
            self.default_template = -1

        self.templates.pop(index)
        print(color('Deleted!', fg='green', bright_fg=True))
        self.save()

    def set_default_template(self, index: int = -1):
        if index == -1:
            for index, template in enumerate(self.templates):
                print(f'{index}: {template.path_to}')

            index = input('Please specify the index of new default template: ')
            while not index.isdigit() and 0 <= int(index) < len(self.templates):
                print(color('Please enter valid index', fg='Red', bright_fg=True))
                index = input('Please specify the index of new default template: ')
            index = int(index)

        self.default_template = index
        self.save()

    def modify_user(self):
        username = input('Enter username:')
        password = getpass('Enter password:')
        self.username = username
        self.password = password
        self.save()
        self.login()

    def login(self):
        client.login(self.username, self.password)


class CodeTemplate(object):
    def __init__(self, lang: Lang = Lang(), path_to: str = '', compile_cmd: str = '', run_cmd: str = '',
                 clean_cmd: str = ''):
        self.lang = lang
        self.path_to = path_to
        self.compile_cmd = compile_cmd
        self.run_cmd = run_cmd
        self.clean_cmd = clean_cmd

    def __str__(self):
        return self.path_to
