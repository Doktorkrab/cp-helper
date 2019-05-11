def choose_yn(text: str, default: bool = True) -> bool:
    print(text, end='')
    if default:
        print('[Y/n]: ', end='')
    else:
        print('[y/N]: ', end='')
    ret = input()
    return ret in 'yY'
