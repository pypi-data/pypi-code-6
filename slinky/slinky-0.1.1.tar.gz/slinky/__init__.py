# -*- coding: utf-8 -*-

__author__ = 'Ben Hughes'
__email__ = 'bwghughes@gmail.com'
__version__ = '0.1.0'

import os
import boto
import click

def create_temp_s3_link(filename, seconds_available, bucket_name):
	connection = boto.connect_s3()
	bucket = connection.get_bucket(bucket_name)
	key = bucket.new_key(filename)
	key.set_contents_from_filename(filename)
	temp_url = key.generate_url(expires_in=seconds_available, query_auth=True)
	return temp_url

@click.command()
@click.argument('filename')
@click.option('--seconds-available', default=3600, type=int)
@click.option('--bucket-name', default='slinky')
@click.option('--aws-key')
@click.option('--aws-secret')
def slinky(filename, seconds_available, bucket_name, aws_key, aws_secret):
    """Simple program that creates an temp S3 link."""
    if not os.environ.get('AWS_ACCESS_KEY_ID') and os.environ.get('AWS_SECRET_ACCESS_KEY'):
    	print 'Need to set environment variables for AWS access'
    	exit()
    
    print create_temp_s3_link(filename, seconds_available, bucket_name)

if __name__ == '__main__':
    print slinky()