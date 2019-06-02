from difflib import ndiff
from os import listdir
from os.path import isfile, splitext, abspath, basename
from subprocess import Popen, PIPE, DEVNULL
from time import time
from typing import List, Tuple

from cf.config.config import CodeTemplate
from utils import color


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


def run_test(code_file: str, template: CodeTemplate) -> None:
    if code_file is None:
        return

    code_file = abspath(code_file)
    in_samples, out_samples = get_samples()
    n = find_samples_number(in_samples, out_samples)
    if n == 0:
        print(color("Can't find any samples! Aborted.", fg='red', bright_fg=True))
        return

    compile_command = prepare_command(template.compile_cmd, code_file)
    print(color(compile_command, fg='blue', bright_fg=True))
    compile_process = Popen(compile_command, stdout=DEVNULL, stderr=PIPE, shell=True)
    try:
        _, stderr = compile_process.communicate(timeout=10)
        stderr = stderr.decode()
    except TimeoutError:
        print(color('Timeout while compilation!', fg='red', bright_fg=True))
        print('Aborting.')
        return
    else:
        if compile_process.poll() != 0:  # return code != 0
            print(color('Compilation runtime error!\n' + 'STDERR:\n' + stderr, fg='red', bright_fg=True))
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
            stdout, stderr = run_process.communicate(input=inp.encode(), timeout=5)
            stdout = stdout.decode()
            stderr = stderr.decode()
        except TimeoutError:
            print(color(f'TL #{num}!', fg='cyan', bright_fg=True))
            return
        else:
            if run_process.poll() != 0:
                print(color('RE #{num}!', fg='red', bright_fg=True))
            if out.strip().rstrip() == stdout.strip().rstrip():
                print(color(f'Ok #{num}.', fg='green', bright_fg=True) + f'... Time: {format(time() - start, ".3f")} secs.')
            else:
                print(color(f'WA #{num}', fg='red', bright_fg=True))
                print('---Input---')
                print(inp)
                print('---Output---')
                print(stdout)
                print('---Right Answer---')
                print(''.join(ndiff(stdout.splitlines(True), out.splitlines(True))))

    clear_command = prepare_command(template.clean_cmd, code_file)
    clear_process = Popen(clear_command, stdin=DEVNULL, stdout=DEVNULL, stderr=PIPE, shell=True)
    try:
        _, stderr = clear_process.communicate(timeout=5)
        stderr.decode()
    except TimeoutError:
        print(color('Timeout on clear command', fg='red', bright_fg=True))
        return
    else:
        if clear_process.poll() != 0:
            print(color('Runtime on clear command\n' + 'STDERR:\n' + stderr.decode(), fg='red', bright_fg=True))

