"""
Master Password command line client.

"""
import click
import pyperclip

from mpw.algorithm import get_password


@click.command()
@click.option('-u', '--user', envvar='MPW_USER',
              help='Full name of the user')
@click.option('-t', '--pwd_type', default='long',
              help='The password template to use (default: long)')
@click.option('-c', '--counter', default=1,
              help='The value for the counter (default: 1)')
@click.argument('site')
def main(site, user, pwd_type, counter):
    """Calculate a site password based on your master password.

    Master password supports the following password types:

    \b
      x, max, maximum  20 characters, contains symbols
      l, long          14 characters, contains symbols
      m, med, medium    8 characters, contains symbols
      b, basic          8 characters, no symbols
      s, short          4 characters, no symbols
      p, pin            4 numbers

    """
    if not user:
        user = click.prompt('Enter your name')

    mpw = click.prompt('Enter master password', hide_input=True)
    pwd = get_password(mpw, user, site, counter, pwd_type)

    # Copy to clipboard
    pyperclip.copy(pwd)
    click.echo('Password for %s for user %s was copied to the clipboard.' %
               (site, user))

if __name__ == '__main__':
    main()
