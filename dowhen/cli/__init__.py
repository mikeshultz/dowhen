import sys
import logging
from argparse import ArgumentParser

from dowhen.common.daemon import run_daemon
from dowhen.common.logger import get_logger, set_level

log = get_logger(__name__)


def create_parser():
    parser = ArgumentParser(
        description="A conditional execution system and scheduler."
    )
    parser.add_argument('-d', '--debug', action='store_true',
                        help="Show extra debugging information")
    parser.add_argument('command', metavar='COMMAND',
                        help="Subocmmand (e.g. daemon)")
    return parser


def parse_args(argv):
    parser = create_parser()
    return parser.parse_args(argv)


def main(argv=None):
    """ Primary CLI entrypoint """
    if argv is None:
        argv = sys.argv[1:]

    args = parse_args(argv)

    if args.debug:
        set_level(logging.DEBUG)

    log.debug(' '.join(sys.argv))

    if args.command == 'daemon':
        log.info('Running daemon...')
        run_daemon()
