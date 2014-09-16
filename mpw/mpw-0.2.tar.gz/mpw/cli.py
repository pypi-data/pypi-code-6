"""
Master Password command line client.

"""
import functools
import time

import click
import pyperclip

import mpw
import mpw.algorithm
import mpw.config


PWD_TYPES = {
    'x': 'max',     'max':   'max',     'maximum': 'max',
    'l': 'long',    'long':  'long',
    'm': 'medium',  'med':   'medium',  'medium':  'medium',
    'b': 'basic',   'basic': 'basic',
    's': 'short',   'short': 'short',
    'p': 'pin',     'pin':   'pin',
}
DEFAULT_USER = mpw.config.load_config()['default']
DEFAULT_USER = ' (default: %s)' % DEFAULT_USER if DEFAULT_USER else ''


def with_config(func):
    """A decorator for automatically loading and writing the configuration.

    It loads the config file, passes the config to the decorated function as
    first argument and writes the config back to the config file after the
    call.

    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        config = mpw.config.load_config()
        ret = func(config, *args, **kwargs)
        mpw.config.write_config(config)
        return ret
    return wrapper


def print_version(ctx, param, value):
    """*Click* callback for printing the program version."""
    if not value or ctx.resilient_parsing:
        return
    click.echo('mpw version %s' % mpw.__version__)
    ctx.exit()


def validate_user(ctx, param, value):
    """If no user was specified, try to get the default user."""
    if value is None:
        value = mpw.config.load_config()['default']
    return value



def validate_pwd_type(ctx, param, value):
    """*Click* callback for validating the ``--pwd-type`` option.

    Either return a valid password type or raise a :exc:`click.BadParameter`.

    """
    try:
        return PWD_TYPES[value]
    except KeyError:
        raise click.BadParameter('Use --help to list valid password types') \
            from None


def validate_counter(ctx, param, value):
    """*Click* callback for validating the ``--counter`` option.

    Either return a valid counter value or raise a :exc:`click.BadParameter`.

    """
    min, max = 1, 0xFFFFFFFF  # min and max for uint32 (4 bytes)
    if not (min <= value <= max):
        raise click.BadParameter('counter not in [%d, %d]' % (min, max))
    return value


@click.group()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True,
              help='Show version number and exit.')
def main():
    """The main entry point for mpw; only prints help and version number."""
    pass


def mpw_command(*args):
    """Decorator that combines ``main.command()``, :func:`with_config()` and
    one :func:`click.argument()` call for every entry in *args*.

    So instead of writing::

        @main.command()
        @with_config
        @click.argument('site')
        @click.argument('user')
        def my_command(config, site, user):
            pass

    you just need to write::

        @mpw_command('site', 'user')
        def my_command(config, site, user):
            pass

    """
    def decorator(func):
        for arg in reversed(args):
            func = click.argument(arg)(func)
        return main.command()(with_config(func))
    return decorator


def option_user():
    """Return a decorator that creates the ``--user`` option for a command."""
    return click.option('-u', '--user',
                        callback=validate_user,
                        help='Full name of the user%s' % DEFAULT_USER)


def option_pwd_type():
    """Return a decorator that creates the ``--pwd-type`` option for a
    command."""
    return click.option('-t', '--pwd_type', default='long',
                        callback=validate_pwd_type,
                        help='The password template to use (default: long)')


def option_counter():
    """Return a decorator that creates the ``--counter`` option for a
    command."""
    return click.option('-c', '--counter', default=1,
                        callback=validate_counter,
                        help='The value for the counter (default: 1)')


def option_account():
    """Return a decorator that creates the ``--account`` option for a
    command."""
    return click.option('-a', '--account', default=None,
                        help='Your account name for this site.')


@mpw_command('site')
@option_user()
@option_pwd_type()
@option_counter()
@option_account()
def get(config, site, user, pwd_type, counter, account):
    """Get a site password.

    Generate a password for SITE and the provided user (or the default user)
    based on your master password.

    Create an entry for user and/or the site in your configuration if they do
    not already exist.

    If the side does not exist yet, you should provide a password type,
    a counter value and the name of your account at the site.

    Master password supports the following password types:

    \b
      x, max, maximum  20 characters, contains symbols
      l, long          14 characters, contains symbols
      m, med, medium    8 characters, contains symbols
      b, basic          8 characters, no symbols
      s, short          4 characters, no symbols
      p, pin            4 numbers

    The counter value can be any positive number.

    """
    if not user:
        user = click.prompt('Enter your name')

    if user not in config['users']:
        mpw.config.add_user(user, config)
        click.echo('Added user "%s".' % user)

    try:
        site_cfg = mpw.config.get_site(site, user, config)
        pwd_type = site_cfg['pwd_type']
        counter = site_cfg['counter']
    except ValueError:
        mpw.config.add_site(site, user, config, pwd_type=pwd_type,
                            counter=counter, account=account)
        click.echo('Added site "%s" for user "%s".' % (site, user))

    password = click.prompt('Enter master password', hide_input=True)
    pwd = mpw.algorithm.get_password(password, user, site, counter, pwd_type)

    # Copy to clipboard
    pyperclip.copy(pwd)
    click.echo('Password for "%s" for user "%s" was copied to the clipboard.' %
               (site, user))


@mpw_command('name')
def adduser(config, name):
    """Add a user."""
    try:
        mpw.config.add_user(name, config)
        click.echo('Added user "%s".' % name)
    except ValueError as e:
        click.echo(e)


@mpw_command('name')
def setuser(config, name):
    """Set a user as default."""
    try:
        mpw.config.set_default_user(name, config)
        click.echo('Set "%s" as default user.' % name)
    except ValueError as e:
        click.echo(e)


@mpw_command('name')
def deluser(config, name):
    """Delete a user."""
    try:
        mpw.config.delete_user(name, config)
        click.echo('User "%s" deleted.' % name)
    except ValueError as e:
        click.echo(e)


@mpw_command()
def users(config):
    """List all users."""
    users = mpw.config.list_users(config)
    for user, is_default in users:
        click.echo('%s%s' % ('*' if is_default else ' ', user))


@mpw_command('site', 'user')
@option_pwd_type()
@option_counter()
@option_account()
def addsite(config, site, user, pwd_type, counter, account):
    """Add a site for a user.

    Master password supports the following password types:

    \b
      x, max, maximum  20 characters, contains symbols
      l, long          14 characters, contains symbols
      m, med, medium    8 characters, contains symbols
      b, basic          8 characters, no symbols
      s, short          4 characters, no symbols
      p, pin            4 numbers

    The counter value can be any positive number.

    """
    try:
        mpw.config.add_site(site, user, config, pwd_type, counter, account)
        click.echo('Added site "%s" for user "%s".' % (site, user))
    except ValueError as e:
        click.echo(e)


@mpw_command('site', 'user')
def getsite(config, site, user):
    """Print site config."""
    try:
        siteconf = mpw.config.get_site(site, user, config)
        strtime = time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(siteconf['access_time']))
        click.echo('Password type: %s' % siteconf['pwd_type'])
        click.echo('Counter value: %d' % siteconf['counter'])
        click.echo('Account name:  %s' % siteconf['account'])
        click.echo('Last access:   %s' % strtime)
    except ValueError as e:
        click.echo(e)


@mpw_command('site', 'user')
@option_pwd_type()
@option_counter()
@option_account()
def updatesite(config, site, user, pwd_type, counter, account):
    """Update the settings for a site.

    Master password supports the following password types:

    \b
      x, max, maximum  20 characters, contains symbols
      l, long          14 characters, contains symbols
      m, med, medium    8 characters, contains symbols
      b, basic          8 characters, no symbols
      s, short          4 characters, no symbols
      p, pin            4 numbers

    The counter value can be any positive number.

    """
    try:
        mpw.config.update_site(site, user, config, pwd_type=pwd_type,
                               counter=counter, account=account)
        click.echo('Updated site "%s" for user "%s".' % (site, user))
    except ValueError as e:
        click.echo(e)


@mpw_command('site', 'user')
def delsite(config, site, user):
    """Delete a site."""
    try:
        mpw.config.delete_site(site, user, config)
        click.echo('Deleted site "%s" for user "%s".' % (site, user))
    except ValueError as e:
        click.echo(e)


@mpw_command('user')
def sites(config, user):
    """List all sites for a user."""
    try:
        sites = mpw.config.list_sites(user, config)
        for site in sites:
            click.echo(site)
    except ValueError as e:
        click.echo(e)
