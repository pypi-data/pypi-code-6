import argparse
import logging

from . import guide
from . import settings


log = logging.getLogger(__name__)


def cli():
    parser = argparse.ArgumentParser(description='Create a CSS/LESS/SASS style guide.')
    # parser.add_argument('fspaths', nargs='+',
        # help="Files or directories.")
    parser.add_argument('-f', '--settingsfile',
        dest='settingsfile', default='vitalstyles.json',
        help='Path to settings file. Defaults to "vitalstyles.json".')
    parser.add_argument('-l', '--loglevel',
        dest='loglevel', default='INFO',
        choices=['DEBUG', 'INFO', 'ERROR'], help='Loglevel.')
    args = parser.parse_args()
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level=getattr(logging, args.loglevel)
    )
    settingsobject = settings.Settings(args.settingsfile)
    guide.Guide(settingsobject).render()


if __name__ == '__main__':
    cli()