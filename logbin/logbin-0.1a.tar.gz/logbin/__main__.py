import argparse
import logging
import sys

from logbin import replay_log


def do_format(args):
    # todo: we need to manually filter on level!

    level = logging.getLevelName(args.level.upper())
    logger = logging.getLogger('')
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    try:
        from nicelog.formatters import ColorLineFormatter
        formatter = ColorLineFormatter(
            show_date=True, show_function=True,
            show_filename=True)
    except:
        formatter = logging.Formatter("%(levelname)s %(msg)s")
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    replay_log(sys.stdin)


def do_format_html(args):
    print("Not supported yet")
    sys.exit(1)


def do_create_dummy_log(args):
    from logbin import PackStreamHandler
    logger = logging.getLogger('')
    logger.addHandler(PackStreamHandler(sys.stdout))

    logger = logging.getLogger('example')
    logger.setLevel(logging.DEBUG)
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')
    try:
        raise ValueError("Example exception")
    except:
        logger.exception("An error happened")

    logger = logging.getLogger('example2')
    logger.setLevel(logging.DEBUG)
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')
    try:
        raise ValueError("Example exception")
    except:
        logger.exception("An error happened")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_format = subparsers.add_parser('format')
    parser_format.add_argument('--level', '-l', default='INFO')
    parser_format.set_defaults(func=do_format)

    parser_format_html = subparsers.add_parser('format_html')
    parser_format_html.add_argument('--level', '-l', default='INFO')
    parser_format_html.set_defaults(func=do_format_html)

    parser_create_dummy_log = subparsers.add_parser('create_dummy_log')
    parser_create_dummy_log.set_defaults(func=do_create_dummy_log)

    args = parser.parse_args(sys.argv[1:])
    args.func(args)


main()
