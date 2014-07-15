import click

# -----------------------------------------------------------------------------
# Validate click options

def file_path(ctx, param, value):
    try:
        open(value, 'r').close()
    except IOError as e:
        raise click.BadParameter('can\'t open %s: (%s)' % (value, e))
    else:
        return value

def regexp(ctx, param, value):
    return r'%s' % value
