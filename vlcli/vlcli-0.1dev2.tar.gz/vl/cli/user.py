import click
import json
import logging
from vl.commands import user as user_cmd


@click.group()
def user():
    """
    User commands
    """
    logger = logging.getLogger(__name__)
    logger.debug('User commands...')
    logger.debug('Checking for user preferences')


@user.command()
@click.option('-n', '--name', prompt=True, help='preferred name')
@click.option('-e', '--email', prompt=True, help='preferred email. this is also the login id')
@click.option('-p', '--password', prompt=True, hide_input=True, confirmation_prompt=True, help='password')
def register(name, email, password):
    """
    Register a new user
    """
    logger = logging.getLogger(__name__)
    logger.debug('Registering user...')
    logger.debug('Name: %s, Email: %s', name, email)

    # click.echo(json.dumps({'name': name, 'email': email}))
    result = user_cmd.register(name, email, password)
    click.echo(json.dumps(result))


@user.command()
@click.option('-e', '--email', help='registered email')
@click.option('-p', '--password', hide_input=True, help='password')
@click.option('-c', '--code', prompt=True, help='activation code')
def activate(email, password, code):
    """
    Activate user
    """
    logger = logging.getLogger(__name__)
    logger.debug('User activation ...')
    logger.debug('Email: %s', email)

    # click.echo(json.dumps({'success': 'user activated'}))
    result = user_cmd.activate(email, password, code)
    click.echo(json.dumps(result))


@user.command('resend-activation')
@click.option('-e', '--email', prompt=True, help='registered email')
@click.option('-p', '--password', prompt=True, hide_input=True, help='password')
def resend_activation(email, password):
    """
    Resend activation code
    """
    logger = logging.getLogger(__name__)
    logger.debug('Resending activation code...')
    logger.debug('Email: %s', email)

    # click.echo(json.dumps({'success': 'activation code resent'}))
    result = user_cmd.resend_activation(email, password)
    click.echo(json.dumps(result))


@user.command()
@click.option('-e', '--email', prompt=True, help='registered email')
@click.option('-p', '--password', prompt=True, hide_input=True, help='password')
def login(email, password):
    """
    Login and cache the credentials
    """
    logger = logging.getLogger(__name__)
    logger.debug('Logging in...')
    logger.debug('Email: %s', email)

    result = user_cmd.login(email, password)
    click.echo(json.dumps(result))


@user.command()
def logout():
    """
    Logout and remove the cached credentials
    """
    logger = logging.getLogger(__name__)
    logger.debug('Logging out...')

    result = user_cmd.logout()
    click.echo(json.dumps(result))


@user.command('forgot-password')
@click.option('-e', '--email', prompt=True, help='registered email')
def forgot_password(email):
    """
    Send password reset code
    """
    logger = logging.getLogger(__name__)
    logger.debug('Forgot password...')
    logger.debug('Email: %s', email)

    # click.echo(json.dumps({'success': 'password reset code sent'}))
    result = user_cmd.forgot_password(email)
    click.echo(json.dumps(result))


@user.command('reset-password')
@click.option('-e', '--email', prompt=True, help='registered email')
@click.option('-n', '--new-password', 'new_password', prompt=True, hide_input=True,
              confirmation_prompt=True, help='password')
@click.option('-c', '--code', prompt=True, help='password reset code')
def reset_password(email, new_password, code):
    """
    Reset password using reset code
    """
    logger = logging.getLogger(__name__)
    logger.debug('Resetting password...')
    logger.debug('Email: %s', email)

    # click.echo(json.dumps({'success': 'password reset'}))
    result = user_cmd.reset_password(email, new_password, code)
    click.echo(json.dumps(result))


@user.command('change-password')
@click.option('-e', '--email', prompt=True, help='registered email')
@click.option('-o', '--old-password', 'old_password', prompt=True, hide_input=True, help='old password')
@click.option('-n', '--new-password', 'new_password', prompt=True, hide_input=True,
              confirmation_prompt=True, help='new password')
def change_password(email, old_password, new_password):
    """
    Change password
    """
    logger = logging.getLogger(__name__)
    logger.debug('Changing password...')
    logger.debug('Email: %s', email)

    # click.echo(json.dumps({'success': 'password changed'}))
    result = user_cmd.change_password(email, old_password, new_password)
    click.echo(json.dumps(result))


@user.command()
@click.option('-e', '--email', prompt=True, help='registered email')
@click.option('-p', '--password', prompt=True, hide_input=True, help='password')
@click.option('-n', '--new-name', 'new_name', help='new name')
@click.option('-m', '--new-email', 'new_email', help='new email')
def update(email, password, new_name, new_email):
    """
    Update user
    """
    logger = logging.getLogger(__name__)
    logger.debug('Updating user...')
    logger.debug('Email: %s, New Name: %s, New Email: %s', email, new_name, new_email)

    # click.echo(json.dumps({'success': 'user updated'}))
    result = user_cmd.update(email, password, new_name, new_email)
    click.echo(json.dumps(result))
