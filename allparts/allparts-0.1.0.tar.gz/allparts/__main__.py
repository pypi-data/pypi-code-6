import click

from allparts.s3merger import S3Merger

@click.command()
@click.argument('bucket')
@click.argument('path')
@click.option('--out', '-o', help="Write output to a file")
def allparts(bucket, path, out):
    merger = S3Merger(bucket, path)
    if out:
        merger.write_file(out)
        print("Wrote output to {out}".format(out=out))
    else:
        print(merger)
