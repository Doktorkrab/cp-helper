from pickle import dump, load
from typing import List

from cp_helper.pcms.config.lang import Lang, _default_lang_list


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
        self.path: str = path
        self.langs: List[Lang] = _default_lang_list
        self.load()

    def load(self) -> None:
        """
        Load Config from file.
        :rtype: None
        """
        with open(self.path, 'rb') as f:
            self.url = load(f)
            self.username = load(f)
            self.password = load(f)
            self.templates = load(f)
            self.default_template = load(f)
            self.langs = load(f)

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
        pass


class CodeTemplate(object):
    def __init__(self, path_to: str = '', compile_command: str = '', run_command: str = '', clean_command: str = '',
                 compilers: List[str] = ''):
        self.path_to: str = path_to
        self.compile_command: str = compile_command
        self.run_command: str = run_command
        self.clean_command: str = clean_command
        self.compilers: List[str] = compilers
