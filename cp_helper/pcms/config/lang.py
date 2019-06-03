from re import findall
from typing import List

from cp_helper.utils import color


class Lang(object):
    def __init__(self, name: str = '', suffix: str = '', id: str = ''):
        self.name = name
        self.id = id
        self.suffix = suffix


_default_lang_list = [Lang("MinGW GCC C++14 7.2.0", ".cpp", "cpp14.gnu"),
                      Lang("Java 8.0 u144", ".java", "java8"),
                      Lang("Python 3.6.2", ".py", "python3"),
                      Lang("Borland Delphi 7.0", ".dpr", "delphi.borland"),
                      Lang("Free Pascal 3.0.2", ".pas", "pascal.free"),
                      Lang("Microsoft Visual C++ 2017", ".cpp", "cpp.visual"),
                      Lang("Python 3.2.5 with PyPy 2.4.0", ".py", "pypy3"),
                      Lang("Microsoft Visual C# 2017", ".cs", "csharp.visual"),
                      Lang("Kotlin 1.1.4-3", ".kt", "kotlin"),
                      Lang("D 2.075.1", ".d", "d")]  # found with find_language


def find_languages(body: str) -> List[Lang]:
    language_select_block = findall(r'''<select id=["']submit:language["']([\s\S]+?)</select>''', body)
    if len(language_select_block) == 0:
        print(color("Can't find any language!", fg='red', bright_fg=True))
        return []
    if len(language_select_block) >= 2:
        print(color("Two select blocks with language options.", fg='red', bright_fg=True))
        return []

    language_select_block = language_select_block[0]
    print(*[f'Lang("{y}", "{z}", "{x}")' for x, y, z in
            findall(r'''<option value=['"]([\S]+?)['"]>([\s\S]+?) \(\*([\S\s]+?)\)''',
                    language_select_block)], sep=',\n')
    return [Lang(y, z, x) for x, y, z in findall(r'''<option value=['"]([\S]+?)['"]>([\s\S]+?) \(\*([\S\s]+?)\)''',
                                                 language_select_block)]
