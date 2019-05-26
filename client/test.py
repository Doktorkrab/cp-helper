from difflib import ndiff
from os import listdir
from os.path import isfile, splitext, abspath, basename
from subprocess import Popen, PIPE, DEVNULL
from time import time
from typing import List, Tuple, Optional

from config import Config
from config.config import CodeTemplate
from utils import choose_yn


def find_samples_number(in_samples: List[int], out_samples: List[int]) -> int:
    cnt = 1
    while cnt in in_samples and cnt in out_samples:
        cnt += 1
    return cnt - 1


def prepare_command(command: str, code_file: str) -> str:
    full_path = abspath(code_file)
    name, extension = splitext(full_path)
    extension = extension[1:]  # remove .
    name = basename(name)

    return command.replace('$%file%$', name).replace('$%ext%$', extension).replace('$%path%$', full_path)


def find_template(file: str) -> Optional[CodeTemplate]:
    cfg = Config()
    _, extension = splitext(file)
    extension = extension[1:]  # remove .

    suitable_templates = []
    for ind, template in enumerate(cfg.templates):
        if template.lang.suffix == extension:
            suitable_templates.append((ind, template))

    if len(suitable_templates) == 0:
        print("[ERROR!] Can't find any suitable template!")
        print("Please add new template for this file extension.")
        print('Or can choose from existing templates')
        if not choose_yn('Choose from existing?'):
            return None
        for num, template in enumerate(cfg.templates):
            print(f'#{num}: {template}')

        chosen = ''
        while not chosen.isdigit() and 0 <= int(chosen) < len(cfg.templates):
            chosen = input('Enter a number:')
        return cfg.templates[int(chosen)]
    elif len(suitable_templates) == 1:
        return suitable_templates[0][1]
    else:
        print('There are some suitable templates.')
        for ind, template in suitable_templates:
            print(f"#{ind}: {template}")

        chosen = ''
        while not chosen.isdigit() and 0 <= int(chosen) < len(cfg.templates):
            chosen = input('Enter a number:')
        return cfg.templates[int(chosen)]


def get_samples() -> Tuple[List[int], List[int]]:
    files = listdir('.')
    in_samples = []
    out_samples = []
    for file in files:
        if not isfile(file):
            continue
        if file.isdigit():
            in_samples.append(int(file))
        elif file.endswith('.a') and file.replace('.a', '').isdigit():
            out_samples.append(int(file.replace('.a', '')))

    in_samples.sort()
    out_samples.sort()
    return in_samples, out_samples


def run_test(code_file: str) -> None:
    code_file = abspath(code_file)
    in_samples, out_samples = get_samples()
    template = find_template(code_file)
    if template is None:
        return
    n = find_samples_number(in_samples, out_samples)
    if n == 0:
        print("[ERROR!] Can't find any samples! Aborted.")
        return

    compile_command = prepare_command(template.compile_cmd, code_file)
    compile_process = Popen(compile_command, stdout=DEVNULL, stderr=PIPE, shell=True)
    try:
        _, stderr = compile_process.communicate(timeout=10)
    except TimeoutError:
        print('[ERROR!] Timeout while compilation!')
        print('Aborting.')
        return
    else:
        if compile_process.poll() != 0:  # return code != 0
            print('[ERROR!] Compilation runtime error!')
            print('STDERR:')
            print(stderr)
            return
    for num in range(1, n + 1):
        with open(f'{num}') as sample:
            inp = sample.read()
        with open(f'{num}.a') as sample:
            out = sample.read()

        run_command = prepare_command(template.run_cmd, code_file)
        run_process = Popen(run_command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        start = time()
        try:
            stdout, stderr = run_process.communicate(input=inp, timeout=5)
        except TimeoutError:
            print(f'TL #{num}!')
            return
        else:
            if run_process.poll() != 0:
                print(f'RE #{num}!')
            if out.strip().rstrip() == stdout.strip().rstrip():
                print(f'Ok #{num}. ... Time: {time() - start} secs.')
            else:
                print(f'WA #{num}')
                print('---Input---')
                print(inp)
                print('---Output---')
                print(stdout)
                print('---Right Answer---')
                print(ndiff(stdout.splitlines(True), out.splitlines(True)))

        clear_command = prepare_command(template.clean_cmd, code_file)
        clear_process = Popen(clear_command, stdin=DEVNULL, stdout=DEVNULL, stderr=PIPE, shell=True)
        try:
            _, stderr = clear_process.communicate(timeout=5)
        except TimeoutError:
            print('[ERROR!] Timeout on clear command')
            return
        else:
            if clear_process.poll() != 0:
                print('[ERROR!] Runtime on clear command!')
                print('---STDERR---')
                print(stderr)