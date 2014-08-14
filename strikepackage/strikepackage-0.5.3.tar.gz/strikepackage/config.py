import os

import kaptan
from yaml.parser import ParserError
from schema import Schema, Use, And, SchemaError

from .utils import abort, warn
from .examples import config_src, userdata_src, metadata_src


def validate_conf(configdata):
    validated = None
    schema = Schema({
        'sp_tag': And(str, len),
        'dns_searchdomain': And(str, len, Use(str.lower)),
        'dns_serverstring': And(str, len, Use(str.lower)),
        'puppet_enable': bool,
        'mchm_enable': bool,
        'hipchat_enable': bool,
        str: object  # don't care about extra data
    })
    try:
        validated = schema.validate(configdata)
    except SchemaError as ex:
        abort("Config file has an invalid or "
              "missing argument: {}".format(ex.message))
    if validated['mchm_enable']:
        validate_conf_mchm(validated)
    if validated['puppet_enable']:
        validate_conf_puppet(validated)
    if validated['hipchat_enable']:
        validate_conf_hipchat(validated)
    return validated


def validate_conf_puppet(params):
    schema = Schema({
        'puppet_url': And(str, len, Use(str.lower)),
        'puppet_environment': And(str, len, Use(str.lower)),
        'puppet_cacert': Use(open),
        'puppet_cert': Use(open),
        'puppet_key': Use(open),
        'puppet_cooldown': And(Use(int), lambda n: 0 <= n <= 3600),
        str: object  # don't care about extra data
    })
    try:
        schema.validate(params)
    except SchemaError as ex:
        abort("Config file has an invalid or "
              "missing argument: {}".format(ex.message))


def validate_conf_mchm(params):
    schema = Schema({
        'mchm_url': And(str, len, Use(str.lower)),
        'mchm_max_polltime': And(Use(int), lambda n: 0 <= n <= 3600),
        'mchm_use_zeroconf': bool,
        'mchm_templatedir': os.path.isdir,
        str: object  # don't care about extra data
    })
    try:
        schema.validate(params)
    except SchemaError as ex:
        abort("Config file has an invalid or "
              "missing argument: {}".format(ex.message))

    # Bail if can't find template files
    for templ in ['userdata.jinja2', 'metadata.jinja2']:
        templ_path = os.path.join(params['mchm_templatedir'], templ)
        if not os.path.isfile(templ_path):
            abort("MCHM is enabled, but couldn't find '{}'. "
                  "See README for help.".format(templ_path))


def validate_conf_hipchat(params):
    schema = Schema({
        'hipchat_api_token': And(str, len),
        'hipchat_roomid': And(str, len),
        'hipchat_from': And(str, lambda n: len(n) < 15),
        str: object  # don't care about extra data
    })
    try:
        schema.validate(params)
    except SchemaError as ex:
        abort("Config file has an invalid or "
              "missing argument: {}".format(ex.message))


def load_args(altconf=None):
    """
    Load arguments from configuration file.
    """
    config = kaptan.Kaptan(handler='yaml')
    mkconfig()

    # If an alternate config file has been specified
    if altconf is not None:
        if not os.path.isfile(altconf):
            abort("File not found: {}".format(altconf))
        try:
            config.import_config(altconf)
        except (ValueError, ParserError):
            abort("{} is not a valid yaml file.".format(altconf))

    # Default
    else:
        conf_dir = os.path.join(os.path.expanduser('~'), '.strikepackage')

        # Look for conf file in default locations
        for loc in [os.curdir, conf_dir]:
            configpath = os.path.join(loc, 'config.yaml')
            try:
                if os.path.isfile(configpath):
                    config.import_config(configpath)
                    break
            except (ValueError, ParserError):
                abort("{} is not a valid yaml file.".format(configpath))
        if not config.configuration_data:
            abort("Config file not found. See README for help.")

    # Validate conf file
    return validate_conf(config.configuration_data)


def mkconfig():
    """
    Places default config dir
    """
    basedir = os.path.join(os.path.expanduser('~'), '.strikepackage')

    # Try to populate dirs
    defaultdirs = [os.path.join(basedir, leaf)
                   for leaf in ['examples', 'keys', 'templates']]

    for dirpath in defaultdirs:
        if not os.path.exists(dirpath):
            try:
                os.makedirs(dirpath, 0755)
            except (os.error, IOError) as ex:
                warn("Error while creating default directory: {}".format(ex))

    # Try to place example confs if not present
    exdir = os.path.join(basedir, 'examples')
    exfiles = [(os.path.join(exdir, exfile[0]), exfile[1])
               for exfile in [('config.yaml', config_src),
                              ('metadata.jinja2', metadata_src),
                              ('userdata.jinja2', userdata_src)]]
    for exfile in exfiles:
        if not os.path.isfile(exfile[0]):
            try:
                with open(exfile[1], 'r') as f:
                    src = f.read()
                with open(exfile[0], 'w+') as f:
                    f.write(src)
            except IOError as ex:
                warn("Error writing example file: {}".format(ex))
