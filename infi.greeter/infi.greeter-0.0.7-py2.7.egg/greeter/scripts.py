import os
import click
import traceback
from infi.traceback import traceback_context


@click.command()
@click.argument('product')
@click.argument('version')
@click.argument('log_path')
@click.argument('setup_status_program')
@click.argument('status_program')
@click.argument('login_program')
@click.option('--terminfo', default='/lib/terminfo', help='terminfo directory')
def greet(product, version, log_path, setup_status_program, status_program, login_program, terminfo):
    """Runs a custom greeter screen.

    PRODUCT is the product name to display

    VERSION is the product version to display

    LOG_PATH is a path to an error log in case the service is not running

    SETUP_STATUS_PROGRAM is a program with arguments to check if the service completed setup (exit 0 - setup complete, otherwise not launching yet)

    STATUS_PROGRAM is a program with arguments to check if the service is running (exit 0 - running, otherwise not)

    LOGIN_PROGRAM is the program to exec when the user chooses LOGIN
    """
    with traceback_context():
        try:
            if 'TERMINFO' not in os.environ:
                os.putenv('TERMINFO', terminfo)
            from . import greet
            return greet(product, version, log_path, setup_status_program, status_program, login_program)
        except:
            traceback.print_exc()
            os._exit(1)


@click.command()
@click.argument('tty_dev')
@click.argument('greeter_path')
def install(tty_dev, greeter_path):
    """Installs a greeter script for a specific tty.

    TTY_DEV is the tty device to install on (tty1, tty2, etc.).

    GREETER_PATH is a path to a greeter executable file (without arguments).
    """
    with traceback_context():
        try:
            from . import install
            install(tty_dev, greeter_path)
        except:
            traceback.print_exc()
            os._exit(1)
