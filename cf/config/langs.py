class Lang(object):
    def __init__(self, name: str = '', suffix: str = '', id: int = -1):
        self.suffix = suffix
        self.name = name
        self.id = id


# TODO: Nerf this
__bad_lang_list = [(43, 'GNU GCC C11 5.1.0', 'c'),
                   (52, 'Clang++17 Diagnostics', 'cpp'),
                   (42, 'GNU G++11 5.1.0', 'cpp'),
                   (50, 'GNU G++14 6.4.0', 'cpp'),
                   (54, 'GNU G++17 7.3.0', 'cpp'),
                   (2, 'Microsoft Visual C++ 2010', 'cpp'),
                   (59, 'Microsoft Visual C++ 2017', 'cpp'),
                   (9, 'C# Mono 5.18', 'cs'),
                   (28, 'D DMD32 v2.083.1', 'd'),
                   (32, 'Go 1.11.4', 'go'),
                   (36, 'Java 1.8.0_162', 'java'),
                   (48, 'Kotlin 1.3.10', 'kt'),
                   (31, 'Python 3.7.2', 'py'),
                   (40, 'PyPy 2.7 (6.0.0)', 'py'),
                   (41, 'PyPy 3.5 (6.0.0)', 'py'),
                   (49, 'Rust 1.31.1', 'rs'),
                   (34, 'JavaScript V8 4.8.0', 'js'),
                   (55, 'Node.js 9.4.0', 'js')]
__bad_lang_list.sort()
lang_list = [Lang(y, z, x) for x, y, z in __bad_lang_list]
