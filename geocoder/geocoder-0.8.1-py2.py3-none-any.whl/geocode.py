import click
import geocoder
import sys
import simplejson as json


@click.command()
@click.argument('f', type=click.File('r'))
@click.argument('output', type=click.File('w'), default='-')
@click.option('--provider', default='google')
def cli(f, output, provider):
    """
    This application will return you the JSON response of a specific geocoding provider.
    The default output is <stdout>
    """
    for line in f.readlines():
        g = geocoder.geocode(line.strip(), provider=provider)
        output.write(json.dumps(g.json) + '\n')