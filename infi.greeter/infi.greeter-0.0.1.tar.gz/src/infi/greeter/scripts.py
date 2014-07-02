import os
import click

@click.command()
@click.argument('product')
@click.argument('version')
@click.argument('log_path')
@click.argument('status_program')
@click.argument('login_program')
@click.option('--terminfo', default='/lib/terminfo', help='terminfo directory')
def main(product, version, log_path, status_program, login_program, terminfo):
    """Runs a custom greeter screen.

    PRODUCT is the product name to display

    VERSION is the product version to display

    LOG_PATH is a path to an error log in case the service is not running

    STATUS_PROGRAM is a program with arguments to check if the service is running (exit 0 - running, otherwise not)

    LOGIN_PROGRAM is the program to exec when the user chooses LOGIN
    """
    if 'TERMINFO' not in os.environ:
        os.putenv('TERMINFO', terminfo)
    from . import greet
    return greet(product, version, log_path, status_program, login_program)


if __name__ == '__main__':
    main()