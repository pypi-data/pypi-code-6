# coding=utf8

"""Usage:
  bell sample configs
  bell <service> [<configs>] [--log-level=<l>]
  bell [-h|-v]

Options:
  -h --help         show this help message
  -v --version      show version
  --log-level=<l>   log level to stdout, 1~5 for CRITICAL~DEBUG [default: 4]

Services:
  listener          listen incomming metrics over tcp
  analyzer          analyze current collected metrics
  webapp            visualize analyzation results on web"""

from docopt import docopt
import toml

from bell import __version__
from bell.analyzer import analyzer
from bell.configs import configs, Configs
from bell.listener import listener
from bell.logger import logger, level_mappings, stdout_handler
from bell.utils import rsync
from bell.webapp import webapp


services = {
    'listener': listener,
    'analyzer': analyzer,
    'webapp': webapp
}


def generate_sample_configs():
    rsync(Configs.default_configs_path, '.')
    logger.info('Generated configs.toml done.')


def initialize_logger(log_level):
    logging_level = level_mappings.get(log_level, level_mappings[4])
    stdout_handler.setLevel(logging_level)


def bootstrap():
    args = docopt(__doc__, version=__version__)

    try:
        log_level = int(args['--log-level'] or 4)
    except ValueError:
        exit(__doc__)
    else:
        initialize_logger(log_level)

    if args['sample'] and args['configs']:
        return generate_sample_configs()

    service_name = args['<service>']

    if service_name in services:
        service = services[service_name]
    else:
        exit(__doc__)

    configs_path = args['<configs>']

    if configs_path:
        try:
            user_configs = toml.loads(open(configs_path).read())
        except (IOError, OSError, toml.TomlSyntaxError) as e:
            logger.error(e)
            exit()
    else:
        user_configs = {}
    configs.update(user_configs)
    service.serve()


if __name__ == '__main__':
    bootstrap()
