from __future__ import unicode_literals

import click
import pkg_resources


@click.group('scaffolding')
def group():
    pass


class Command(object):

    verbosity = 0

    class options(object):
        simulate = False
        interactive = False
        overwrite = True


@group.command()
@click.argument('template')
@click.argument('destination')
def create(template, destination):
    template = [
        scaffold for scaffold in all_scaffolds() if scaffold.name == template
    ][0]
    variables = {
        'project': destination,
        'package': destination,
        'egg': destination,
        'pyramid_version': '1.3.1',
        'pyramid_docs_branch': 'latest',
    }

    template.run(Command, destination, variables)


@group.command('list')
def list_scaffolding():
    for scaffold in all_scaffolds():
        click.echo(scaffold.name + '\t' + scaffold.summary)


def all_scaffolds():
    scaffolds = []
    eps = list(pkg_resources.iter_entry_points('pyramid.scaffold'))
    for entry in eps:
        try:
            scaffold_class = entry.load()
            scaffold = scaffold_class(entry.name)
            scaffolds.append(scaffold)
        except Exception as ex:  # pragma: no cover
            click.echo(
                'Warning: could not load entry point %s (%s: %s)' % (
                    entry.name, ex.__class__.__name__, ex
                )
            )
    return scaffolds
