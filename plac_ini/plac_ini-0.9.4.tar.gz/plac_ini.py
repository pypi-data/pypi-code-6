import sys

# defaults are defined by the function
# defaults are overridden with values from config file
# defaults and config file are overridden with command line parameters

def _read_config(config, default_section=None):
    try:
        import configparser
    except ImportError:
        import ConfigParser as configparser

    if sys.version >= '3':
        cp = configparser.SafeConfigParser()
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
            cp = configparser.SafeConfigParser()
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

def call(obj, arglist=sys.argv[1:], eager=True, config=None,
         default_section=None):
    import plac

    if config is None:
        return plac.call(obj, arglist=arglist, eager=eager)

    try:
        from itertools import zip_longest
    except ImportError:
        from itertools import izip_longest as zip_longest

    argparser = plac.parser_from(obj)
    argnames = argparser.argspec.args
    defaults = argparser.argspec.defaults

    cfg = dict(zip_longest(argnames, defaults))
    cfg.update(_read_config(config, default_section))
    if sys.version >= '3':
        items = cfg.items()
    else:
        items = cfg.iteritems()
    argparser.set_defaults(**dict((k, v) for k, v in items))
    cmd, result = argparser.consume(arglist)

    if plac.iterable(result) and eager: # listify the result
        return list(result)
    return result

