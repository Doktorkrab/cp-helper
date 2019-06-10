from os import makedirs
from os.path import isfile, expanduser, abspath, basename
from pickle import dump, load
from typing import List

from cp_helper.pcms.client.login import login
from cp_helper.pcms.config.lang import Lang, _default_lang_list
from cp_helper.utils import choose_yn

SESSION_PATH = expanduser('~/.cpSessionPcms/')


class Config(object):
    """
    Class, that contains main config values.
    There are two types of config: main config(~/.cpConfigPcms/*) and config from current contest folder
    """

    def __init__(self, path: str):
        self.url: str = ''
        self.username: str = ''
        self.password: str = ''
        self.templates: List[CodeTemplate] = []
        self.default_template: int = -1
        self.path: str = expanduser(path)
        self.langs: List[Lang] = _default_lang_list
        self.load()

    def __str__(self):
        ret = ''
        ret += f'url: {self.url}\n'
        ret += f'username: {self.username}\n'
        ret += f'templates:\n'
        max_len = len(str(len(self.templates)))

        for i in range(len(self.templates)):
            need_spaces = max_len - len(str(i + 1))
            ret += f"{' ' * need_spaces}#{i + 1}|{self.templates[i].path_to}\n"
            ret += f"{' ' * max_len} |{self.templates[i].compile_command}\n"
            ret += f"{' ' * max_len} |{self.templates[i].run_command}\n"
            ret += f"{' ' * max_len} |{self.templates[i].clean_command}\n"
            ret += f"{' ' * max_len} |{', '.join([str(x) for x in self.templates[i].compilers])}\n"
        ret += f'Path to config:{self.path}\n'
        sep = ',\n'
        ret += f'Langs: {sep.join([str(x) for x in self.langs])}'
        return ret

    def load(self) -> None:
        """
        Load Config from file.
        :rtype: None
        """
        try:
            with open(self.path, 'rb') as f:
                self.url = load(f)
                self.username = load(f)
                self.password = load(f)
                self.templates = load(f)
                self.default_template = load(f)
                self.langs = load(f)
        except FileNotFoundError:
            pass

    def save(self) -> None:
        """
        Save config to file
        :return: None
        :rtype None
        """
        with open(self.path, 'wb') as f:
            dump(self.url, f)
            dump(self.username, f)
            dump(self.password, f)
            dump(self.templates, f)
            dump(self.default_template, f)
            dump(self.langs, f)

    def add_template(self) -> None:
        """
        Add a new template to Config
        :return: None
        :rtype: None
        """
        to_add = CodeTemplate()
        max_len = len(str(len(self.langs)))
        print('There are available langs:')
        for i in range(len(self.langs)):
            needs_spaces = max_len - len(str(i + 1))
            print(f"{' ' * needs_spaces}#{i + 1}|{self.langs[i]}")

        chosen = input('Please enter a index:')
        while not chosen.isdigit() or not (1 <= int(chosen) <= len(self.langs)):
            chosen = input('Please enter a correct index:')
        to_add.compilers.append(self.langs[int(chosen) - 1])

        correct = False
        while not correct:
            to_add.path_to = abspath(
                expanduser(input('Enter path to template(e.g ~/template.cpp, template.py, may be empty)')))

            if isfile(to_add.path_to):
                with open(to_add.path_to) as f:
                    print(f'{to_add.path_to}:\n{f.read()}')
            else:
                print(f"{to_add.path_to}:Not a file")
            correct = choose_yn('Is this correct file?')

        print('There are available aliases for next commands')
        print('$%full%$ - full file name(e.g. code_file.cpp)')
        print('$%file%$ - file name(e.g. code_file)')
        print('$%ext%$ - extension of file(e.g. .cpp)')

        to_add.compile_command = input('\nPlease enter command to compile. May be empty:')
        to_add.run_command = input('Please enter command to run:')
        while not to_add.run_command:
            to_add.run_command = input('Please enter command to run. Cannot be empty:')
        to_add.clean_command = input('Please enter command, that runs after testing(e.g. rm $%file%$). May be empty:')

        self.templates.append(to_add)

        if choose_yn('Set it default?'):
            self.default_template = len(self.templates) - 1

        self.save()

    def delete_template(self):
        max_len = len(str(len(self.templates)))

        for i in range(len(self.templates)):
            need_spaces = max_len - len(str(i + 1))
            print(f"{' ' * need_spaces}#{i + 1}|{self.templates[i].path_to}")
            print(f"{' ' * max_len} |{self.templates[i].compile_command}")
            print(f"{' ' * max_len} |{self.templates[i].run_command}")
            print(f"{' ' * max_len} |{self.templates[i].clean_command}")
            print(f"{' ' * max_len} |{', '.join([str(x) for x in self.templates[i].compilers])}")

        chosen = input('Please enter a index:')
        while not chosen.isdigit() or not (0 < int(chosen) <= len(self.templates)):
            chosen = input('Please enter a correct index:')

        if not choose_yn('Are you sure?'):
            return

        if int(chosen) - 1 < self.default_template:
            self.default_template -= 1
        elif int(chosen) - 1 == self.default_template:
            self.default_template = -1

        self.templates.pop(int(chosen) - 1)

        self.save()

    def login(self, username: str = '', password: str = ''):
        if username:
            self.username = username
        if password:
            self.password = password

        makedirs(SESSION_PATH, exist_ok=True)
        login(self.username, self.password, SESSION_PATH + basename(self.path), self.url)

        self.save()


class CodeTemplate(object):
    def __init__(self, path_to: str = '', compile_command: str = '', run_command: str = '', clean_command: str = '',
                 compilers=None):
        if compilers is None:
            compilers = []
        self.path_to: str = path_to
        self.compile_command: str = compile_command
        self.run_command: str = run_command
        self.clean_command: str = clean_command
        self.compilers: List[Lang] = compilers  # compilers for various contests
