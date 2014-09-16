"""
This module implements the user and site management and stores users/sites in
a config file.

"""
import json
import os
import time

import click


APP_NAME = 'Master Password'
CFG_FILE = 'config.json'


def add_user(name, config):
    """Add user *name*  to *config* and set as default.

    Raise a :exc:`ValueError` if *name* already exists.

    """
    if name in config['users']:
        raise ValueError('User "%s" already exists.' % name)

    config['users'][name] = {}
    set_default_user(name, config)


def delete_user(name, config):
    """Delete user *name* from *config*.

    Raise a :exc:`ValueError` if *name* does not exist.

    """
    _check_user(name, config)

    del config['users'][name]
    if config['default'] == name:
        config['default'] = None


def set_default_user(name, config):
    """Set *name* as default user in *config*.

    Raise a :exc:`ValueError` if *name* does not exist.

    """
    _check_user(name, config)

    config['default'] = name


def list_users(config):
    """Return a sorted list of tuples ``(user_name, is_default)`` from the
    *config*."""
    return [(name, name == config['default'])
            for name in sorted(config['users'])]


def add_site(name, user, config, pwd_type, counter, account=None):
    """Add the site *name* for *user* to its *config* and set the *pwd_type*,
    *counter* value and, optionally, the login name *account*."""
    _check_user(user, config)

    if name in config['users'][user]:
        raise ValueError('Site "%s" for user "%s" already exists.' %
                         (name, user))

    config['users'][user][name] = {
        'pwd_type': pwd_type,
        'counter': counter,
        'account': account,
        'access_time': time.time(),
    }


def update_site(name, user, config, **kwargs):
    """Update the access time for the site *name* for *user* in *config*."""
    _check_user_and_site(user, name, config)

    siteconf = config['users'][user][name]
    for key, val in siteconf.items():
        if key in kwargs:
            siteconf[key] = kwargs[key]
    siteconf['access_time'] = time.time()


def get_site(name, user, config):
    """Get the site config for *name* for *user* from *config*."""
    _check_user_and_site(user, name, config)
    return config['users'][user][name]


def delete_site(name, user, config):
    """Delete the site *name* for *user* from config."""
    _check_user_and_site(user, name, config)
    del config['users'][user][name]


def list_sites(user, config):
    """Get the sites for *user* from *config* sorted by access time in
    descending order."""
    _check_user(user, config)
    return [name for name, data in sorted(config['users'][user].items(),
                                          key=lambda s: s[1]['access_time'],
                                          reverse=True)]


def load_config():
    """Return the configuration from the config file.

    If the config file does not exist, create it and populate it with default
    values.

    The return value is a dictionary with the following keys:

    - *default* contains the default user name or ``None``
    - *users* is a dictionary mapping user names to their list of configured
      sites.

    """
    try:
        cfg_file = _get_config_filename()
        with open(cfg_file, 'r') as fp:
            config = json.load(fp)
    except FileNotFoundError:
        config = {
            'default': None,
            'users': {},
        }
    return config


def write_config(config):
    """Write the *config* to the config file."""
    cfg_file = _get_config_filename()
    with open(cfg_file, 'w') as fp:
        json.dump(config, fp, indent=4)


def _get_config_filename():
    """Return the config file name and ensure its parent directory exists."""
    app_dir = click.get_app_dir(APP_NAME)
    if not os.path.isdir(app_dir):
        os.mkdir(app_dir, mode=0o755)
    return os.path.join(app_dir, CFG_FILE)


def _check_user(user, config):
    """Check if *user* are in *config* and raise a :exc:`ValueError` if not."""
    if user not in config['users']:
        raise ValueError('User "%s" does not exist.' % user)


def _check_user_and_site(user, site, config):
    """Check if *user* and *site* are in *config* and raise a :exc:`ValueError`
    if not."""
    if user not in config['users']:
        raise ValueError('User "%s" does not exist.' % user)

    if site not in config['users'][user]:
        raise ValueError('Site "%s" for user "%s" does not exist.' %
                         (site, user))
