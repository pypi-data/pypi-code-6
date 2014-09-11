from ftplib import FTP
from urllib2 import Request, urlopen
from os.path import isdir, isfile
from os import mkdir
import urllib
import re

from bs4 import BeautifulSoup
import requests


def download_state_shapes(outdir='shapefiles'):
    return download_shapefiles_from_census(type='STATE', outdir=outdir, outprefix='state')


def download_city_shapes(outdir='shapefiles'):
    return download_shapefiles_from_census(type='PLACE', outdir=outdir, outprefix='city')


def download_zip_shapes(outdir='shapefiles'):
    return download_shapefiles_from_census(type='ZCTA5', outdir=outdir, outprefix='zip')


# type should be one of PLACE, STATE, or ZCTA5
def download_shapefiles_from_census(type, outdir, outprefix):
    if not isdir(outdir):
        mkdir(outdir)

    census = FTP('ftp2.census.gov')
    print "Acquiring connection to census.gov"
    census.login()
    print "Connected!"
    filenames = census.nlst('geo/tiger/TIGER2013/%s' % type)

    for ftp_filename in filenames:
        zip_filename = re.match('.*/(.*\.zip)', ftp_filename).group(1)
        zip_filepath = '%s/%s%s' % (outdir, outprefix, zip_filename)

        if not isfile(zip_filepath):
            print 'Downloading %s' % zip_filename
            req = Request('ftp://ftp2.census.gov/%s' % ftp_filename)
            res = urlopen(req)
            with open(zip_filepath, 'a') as out:
                out.write(res.read())
        else:
            print '%s already exists. Skipping download' % zip_filepath

    census.close()

    return outdir


def download_neighborhood_shapes(outdir='shapefiles', outprefix='neighborhood'):
    zillow_neighborhoods_url = 'http://www.zillow.com/howto/api/neighborhood-boundaries.htm'
    result = requests.get(zillow_neighborhoods_url)
    soup = BeautifulSoup(result.text)
    links = [e.get('href') for e in soup.select('.illo-block ul a')]

    url_prefix = 'http://www.zillow.com'
    state_re = re.compile('-(.*?.zip)$')

    if not isdir(outdir):
        mkdir(outdir)

    f = urllib.URLopener()
    for link in links:
        state = state_re.search(link).group(1)
        filename = '%s/%s%s.zip' % (outdir, outprefix, state)

        if isfile(filename):
            print "%s already exists. Skipping..." % filename
            continue

        try:
            url = "%s%s" % (url_prefix, link)
            f.retrieve(url, filename)
        except IOError:
            print "Error retrieving zip file: %s" % url

    return outdir
