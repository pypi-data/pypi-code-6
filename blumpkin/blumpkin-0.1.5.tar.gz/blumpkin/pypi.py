from __future__ import unicode_literals

import click
import os


@click.command('create-pypi')
@click.argument('username', nargs=1)
@click.argument('password', nargs=1)
@click.argument('index', nargs=1)
@click.option('--base-dir', nargs=1, default='~/')
@click.option('--dry', nargs=1, type=bool, default=False)
def create_pypi(username, password, index, base_dir, dry):
    root = os.path.expanduser(base_dir + '.pip')

    if not dry:
        os.path.exists(root) or os.mkdir(root)

    for file_path, contents in (
        (
            os.path.join(root, 'pip.conf'),
            [
                '[global]',
                'extra-index-url = https://{}:{}@{}'.format(
                        username, password, index
                )
            ]
        ),
        (
            os.path.join(os.path.expanduser(base_dir), '.pypirc'),
            [
                '[distutils]',
                'index-servers=',
                '\tpypi',
                '\tbalanced',
                '',
                '[balanced]',
                '\trepository: {}'.format(index),
                '\tusername: {}'.format(username),
                '\tpassword: {}'.format(password)
            ]
        ),
        (
            os.path.join(os.path.expanduser(base_dir), '.pydistutils.cfg'),
            [
                '[easy_install]',
                'index_url = https://{}:{}@{}'.format(
                        username, password, index
                )
            ]
        )
    ):
        with open(file_path, 'w') as f:
            if dry:
                print ''
                print file_path
            for line in contents:
                if dry:
                    print line
                f.write(line)
                f.write('\n')
            if not dry:
                click.echo('wrote {}'.format(file_path))

    click.echo('created pypi setup files')
