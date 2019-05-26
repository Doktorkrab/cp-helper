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
