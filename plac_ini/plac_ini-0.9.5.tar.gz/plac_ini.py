import sys

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

import argparse

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

import plac

if sys.version >= '3':
    from inspect import getfullargspec
else:
    from plac import getfullargspec


# defaults are defined by the function
# defaults are overridden with values from config file
# defaults and config file are overridden with command line parameters

CONFIG_PARSER_CFG = getfullargspec(ConfigParser.__init__).args[1:]
# the default arguments accepted by a ConfigParser object

def config_conf(obj):
    "Extracts the configuration of the underlying ConfigParser from obj"
    # If we ever want to add some default options this is where to do that
    cfg = {}
    for name in dir(obj):
        if name in CONFIG_PARSER_CFG: # argument of ConfigParser
            cfg[name] = getattr(obj, name)
    return cfg


def config_parser_from(obj, config, default_section=None, **confparams):
    conf = config_conf(obj)
    conf.update(confparams)
    parser = ConfigParser(**conf)
    parser.plac_ini_obj = obj
    parser.plac_ini_config = config
    parser.plac_ini_default_section = default_section
    return parser


def _read_config(cp, config, default_section=None):
    if sys.version >= '3':
        try:
            with open(config) as fp:
                cp.readfp(fp)
        except FileNotFoundError:
            # consider raising an exception here.
            # but, tools may operate fine without a config file.
            return {}
    else:
        from StringIO import StringIO
        try:
            # this is needed in Python 2 to work with some kinds of ini files
            data = StringIO('\n'.join(line.strip() for line in open(config)))
            cp.readfp(data)
        except IOError:
            # consider raising an exception here.
            # but, tools may operate fine without a config file.
            return {}

    cfg = {}
    for section in cp.sections():
        if default_section is not None and default_section == section:
            prefix = ''
        else:
            prefix = '%s_' % section
        for k, v in cp.items(section):
            cfg['%s%s' % (prefix, k)] = v
    return cfg


def add_gnu_argument(self, *args, **kwargs):
    "Prevent the addition of any single hyphen, multiple letter args"

    gnu_args = []

    for arg in args:
        # Fix if we have at least 3 chars where the first is a hyphen
        # and the second is not a hyphen (e.g. -op becomes --op)
        if len(arg) > 3 and arg[0] == '-' and arg[1] != '-':
            gnu_args.append('-' + arg)
        else:
            gnu_args.append(arg)

    argparse.ArgumentParser.add_argument(self, *gnu_args, **kwargs)

def _print_exit(message, file=None):
    if message:
        if file is None:
            file = sys.stderr
        file.write(message)
    sys.exit(2)

def call(obj, arglist=sys.argv[1:], eager=True, config=None,
         default_section=None, gnu=True):
    if gnu:
        plac.ArgumentParser.add_argument = add_gnu_argument

    if config is None:
        return plac.call(obj, arglist=arglist, eager=eager)

    argparser = plac.parser_from(obj)
    argnames = argparser.argspec.args
    defaults = argparser.argspec.defaults

    cp = config_parser_from(obj, config, default_section)

    cfg = dict(zip_longest(argnames, defaults))
    ini_values = _read_config(cp, config, default_section)

    for k in obj.__annotations__.keys():
        a = plac.Annotation.from_(obj.__annotations__[k])
        if a.type and k in ini_values:
            if a.type is type(True):
                try:
                    ini_values[k] = cp._convert_to_boolean(ini_values[k])
                except ValueError:
                    argparser.print_usage(sys.stderr)
                    _print_exit(
                        "{}: error: {}={} failed conversion to <type 'bool'> in:\n{}\n".format(
                            argparser.prog, k, ini_values[k], config))
            else:
                try:
                    ini_values[k] = a.type(ini_values[k])
                except ValueError:
                    argparser.print_usage(sys.stderr)
                    _print_exit(
                        '{}: error: {}={} failed conversion to {} in:\n{}\n'.format(
                            argparser.prog, k, ini_values[k], a.type, config))

    cfg.update(ini_values)

    if sys.version >= '3':
        items = cfg.items()
    else:
        items = cfg.iteritems()
    argparser.set_defaults(**dict((k, v) for k, v in items))
    cmd, result = argparser.consume(arglist)

    if plac.iterable(result) and eager: # listify the result
        return list(result)
    return result

