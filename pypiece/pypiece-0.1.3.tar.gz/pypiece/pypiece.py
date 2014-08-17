# coding: utf-8

import click
import os
import subprocess


class VenvNotFoundError(Exception):
    pass


class PipNotFoundError(Exception):
    pass


def fatal(msg, **kwargs):
    txt = msg.format(**kwargs)
    click.echo(click.style(txt, fg="red"))
    exit(-1)


@click.command()
@click.argument('req_file')
@click.argument('pip_opts', nargs=-1)
@click.option('--retries', '-r', default=3, show_default=True,
              help='Number of repeated attempts to install package.')
@click.option('--pip', '-p', default='pip', show_default=True,
              help='Specify pip binary to use.')
@click.option('--venv', '-v', default=None, show_default=True,
              help='virtualenv to install packages into.')
def piecemeal_install(req_file, pip, pip_opts, retries, venv):
    u'''
    Install packages from provided requirements file piece by piece.
    If package installation fails, continue like nothing happened.
    '''

    def show_item(item):
        if item is not None:
            return click.style(item, fg="blue")

    failed_packages = []
    success_packages = []
    already_installed = []

    if pip != 'pip' and venv:
        raise ValueError("--pip and --venv options should not be specified at the same time!")

    if venv:
        # If virtualenv name specified, try to get root directory from environment
        # (only works with virtualenvwrapper for the moment).
        workon_home = os.environ.get('WORKON_HOME', '')
        if not workon_home:
            raise VenvNotFoundError("virtualenv specified, but no WORKON_HOME "
                             "environment valuable found!")

        venv_pip = os.path.join(workon_home, venv, 'bin', 'pip')
        if not os.path.exists(venv_pip):
            raise PipNotFoundError("Virtualenv '{}' is not found!".format(venv))
        pip = venv_pip

    with open(req_file, 'r') as fp:
        # Load up requirements and filter out comments
        lines = [l.strip() for l in fp.readlines() if not l.startswith('#')]
        # Normalize requirements list, skipping blank lines
        lines = filter(lambda x: x, list(set(lines)))

        with click.progressbar(lines,
                               label="Processing packages",
                               bar_template="%(label)s [%(bar)s] %(info)s",
                               item_show_func=show_item,
                               show_eta=False,
                               fill_char=click.style('#', fg='green')) as packages:
            for package in packages:
                cmd = [pip, 'install', package]
                cmd.extend(pip_opts)
                success = False

                for attempt in xrange(1 + retries):
                    try:
                        # Run 'pip' and capture its output for further analysis
                        output = subprocess.check_output(cmd)
                        if output.startswith('Requirement already satisfied'):
                            # It seems that requirement was already satisfied
                            already_installed.append(package)
                        elif 'Successfully installed' in output:
                            # Requirement was installed successfully
                            # FIXME: Triggers on reinstallation of dependent package
                            # TODO: Record dependent packages
                            success_packages.append(package)
                        success = True
                        break
                    except subprocess.CalledProcessError as call_exc:
                        # Something went wrong, note it and carry on
                        pass

                if not success:
                    failed_packages.append(package)

    for title, color, affected in (
            ('Already installed', 'blue', already_installed),
            ('Installed', 'green', success_packages),
            ('Failed', 'red', failed_packages)):
        if affected:
            click.echo()
            click.echo(click.style('[{0}]'.format(title), fg=color))
            click.echo('\n'.join(affected))


if __name__ == '__main__':
    try:
        piecemeal_install()
    except Exception as exc:
        fatal(unicode(exc))
