import os
import ConfigParser

import click


def set_default_tag(tag):
    if not tag:
        tag = 'default'

    return tag


def parse_tag(tag):
    if isinstance(tag, tuple):
        tag = ','.join(tag)

    return tag


def create_config(tag):
    config = ConfigParser.RawConfigParser()
    config.add_section('tags')
    config.set('tags', 'tags', tag)

    return config


def create_config_file(directory):
    fid = open(os.path.join(directory, '.pymr'), 'wb')

    return fid


def write_config_to_file(fid, config):
    config.write(fid)
    fid.close()


@click.command()
@click.option('--directory', '-d', default='./')
@click.option('--tag', '-t', multiple=True)
def register(directory, tag):
    """
    register a directory for use with pymr \n
    example: pymr-register -d ./ -t foo -t bar
    """
    print 'Creating file .pymr in {0}'.format(directory)

    tag = set_default_tag(tag)
    tag = parse_tag(tag)
    config = create_config(tag)
    fid = create_config_file(directory)
    write_config_to_file(fid, config)
