from cp_helper.pcms.cmd.config import parse_config


def parse_args(args: dict) -> None:
    """
    Function to parse docopt args/
    :param args: Args to parse
    :return: None
    """
    if args['config']:
        parse_config(args)
