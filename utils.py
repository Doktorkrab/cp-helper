from typing import List


def choose_yn(text: str, default: bool = True) -> bool:
    print(text, end='')
    if default:
        print('[Y/n]: ', end='')
    else:
        print('[y/N]: ', end='')
    ret = input()
    return ret in 'yY'


def pretty_test_num(number: int, max_number: int) -> str:
    return '0' * (len(str(max_number)) - len(str(number))) + str(number)


def color(s: str, fg: str = '', bg: str = '', bright_fg: bool = False, bright_bg: bool = False, bold: bool = False,
          underline: bool = False) -> str:
    csi = '\u001b[;'
    fg = fg.lower()
    bg = bg.lower()

    order = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

    ret = ''
    if fg:
        ret += csi + '3' + str(order.index(fg)) + (';1' if bright_fg else '') + 'm'
    if bg:
        ret += csi + '4' + str(order.index(bg)) + (';1' if bright_bg else '') + 'm'
    if bold:
        ret += csi + '1m'
    if underline:
        ret += csi + '4m'
    ret += s
    return ret + csi + '0m'
