import click


class Logger:

    def __init__(self, verbose):
        self.verbose = verbose

    def debug(self, message, **kwargs):
        if self.verbose > 0:
            click.secho(message, fg='blue')

    def info(self, message, **kwargs):
        click.secho(message, fg='green')
