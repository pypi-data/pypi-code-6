import logging, logging.handlers, logging.config
from socket import error as socket_error
from datetime import datetime

DEFAULT_ROOT_LOG_LEVEL = 'ERROR'
LOG_LEVEL_NAMES = ['DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'CRITICAL']


def parse_log_level(arg):
    """
    Parse a `module=level` log level argument into a module name and a log
    level (as identifiable by the logging module).

    Also accepts simply `level` to set the log level of the root logger, in
    which case it returns None as the module name.
    """
    if '=' in arg:
        mod, level = arg.split('=', 1)
    else:
        mod = None
        level = arg
    if level.upper() not in LOG_LEVEL_NAMES:
        raise ValueError("Invalid log level: " + level)
    return mod, level.upper()

def valid_log_level(arg):
    """
    Parses the log level to ensure that it's valid, but just returns
    the original string.
    """
    # The following call is only for its error-raising side effects.
    parse_log_level(arg)
    return arg


def add_argparse_group(parser):
    """Add a configuration group for plumb_util to an argparser"""
    log_level_help = (
        'Set the logging level. A bare level (e.g., "warn") sets the level of '
        'the root logger (defaults to "error"); arguments of the form '
        '"module=level" set the logging level for a particular module (and its '
        'descendents, unless configured otherwise)')
    group = parser.add_argument_group('find_service', 'SRV lookup configuration')
    zone_group = group.add_mutually_exclusive_group()
    zone_group.add_argument('-Z', '--zone', type=str, default=None,
                            help='DNS zone to consult for service autodiscovery.')
    zone_group.add_argument('-D', dest='zone', type=str, default=None,
                            help='DNS zone to consult for service autodiscovery.')
    group.add_argument('-L', '--loglevel', action='append',
                       default=[], type=valid_log_level,
                       help=log_level_help)


def serialize_log_args(log_level_args):
    """
    Return a version of the logging arguments suitable to pass on to
    another process also using this module.
    """
    args = []
    for arg in log_level_args:
        args.extend(['-L', arg])
    return args


# logging.Formatter insists on time tuples (which don't contain sub-second
# resolution), and strftime format strings don't allow you to specify precision
# on the microseconds.  So we need to subclass.  Annoying.
class MillisecondLogFormatter(logging.Formatter):
    def formatTime(self, record, dateFmt):
        assert dateFmt.endswith('%f')
        return datetime.fromtimestamp(record.created).strftime(dateFmt)[:-3]


def init_logging(procname, config_dict):
    root_logger = logging.root
    str_fmt = '%(asctime)s ' + procname + ': ' + logging.BASIC_FORMAT
    date_fmt = '%b %d %H:%M:%S.%f'
    log_fmt = MillisecondLogFormatter(str_fmt, date_fmt)

    stderr_handler = logging.StreamHandler()
    stderr_handler.setFormatter(log_fmt)
    root_logger.addHandler(stderr_handler)

    try:
        syslog_handler = logging.handlers.SysLogHandler(
            address='/dev/log',
            facility=logging.handlers.SysLogHandler.LOG_LOCAL0)
    except socket_error:
        root_logger.warn('unable to initialize syslog logger')
    else:
        syslog_handler.setFormatter(log_fmt)
        root_logger.addHandler(syslog_handler)

    # Use the config_dict to only update the log levels.
    logging.config.dictConfig(dict(
            config_dict, incremental=True, version=1))

    return root_logger

def logger_from_args(args, procname):
    levels = {None: DEFAULT_ROOT_LOG_LEVEL}
    levels.update(map(parse_log_level, args.loglevel))
    if LOG_LEVEL_NAMES.index(levels[None]) < LOG_LEVEL_NAMES.index('WARN'):
        levels.setdefault('stomp', 'WARN')

    config_dict = {'root': {'level': levels.pop(None)}}
    config_dict['loggers'] = {module: {'level': level}
                              for module, level in levels.items()}

    return init_logging(procname, config_dict)

