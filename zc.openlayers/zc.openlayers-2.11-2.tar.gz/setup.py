# This is very fragile.
#
# An sdist built from this doesn't include the resources, but an egg
# built from the sdist works just fine.

import os
import setuptools
import shutil
import tarfile
import urllib2

# The OpenLayers version:
VERSION = "2.11"

# zc.openlayers version (increment on release, reset when VERSION changes):
RELEASE = 2

try:
    here = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Somebody didn't populate __file__!
    here = os.getcwd()

resources = os.path.join(here, "src", "zc", "openlayers", "resources")
url = ("https://github.com/openlayers/openlayers/releases/download/release-%s"
       "/OpenLayers-%s.tar.gz" % (VERSION, VERSION))


def copy(src, dst):
    if os.path.isfile(dst):
        os.unlink(dst)
    elif os.path.isdir(dst):
        shutil.rmtree(dst)

    if os.path.isfile(src):
        shutil.copy(src, dst)
    else:
        shutil.copytree(src, dst)


def fetch(url, dest):
    inf = urllib2.urlopen(url)
    outf = open(dest, "wb")
    shutil.copyfileobj(inf, outf)
    inf.close()
    outf.close()


tmpdir = os.path.join(here, "tmp")
os.mkdir(tmpdir)
os.chdir(tmpdir)
try:
    # Download the package:
    fetch(url, "OpenLayers.tar.gz")

    # Unpack:
    # We can't use extractall() since that's new in Python 2.5.
    # This could be smarter, but let's not worry about that.
    tf = tarfile.open("OpenLayers.tar.gz")
    while True:
        fi = tf.next()
        if fi is None:
            break
        if fi.isdir():
            path = os.path.join(tmpdir, fi.name)
            os.makedirs(path)
        else:
            tf.extract(fi, tmpdir)
    tf.close()

    if not os.path.exists(resources):
        # This directory doesn't actually doesn't get packaged, at least
        # when subversion 1.6 is being used on the client.
        os.mkdir(resources)

    # Copy the interesting bits:
    openlayers = "OpenLayers-" + VERSION
    copy(
        os.path.join(openlayers, "lib", "Firebug"),
        os.path.join(resources, "Firebug"))
    copy(
        os.path.join(openlayers, "OpenLayers.js"),
        os.path.join(resources, "OpenLayers.js"))
    copy(
        os.path.join(openlayers, "img"),
        os.path.join(resources, "img"))
    copy(
        os.path.join(openlayers, "theme"),
        os.path.join(resources, "theme"))
    fetch(
        # Not sure how this is managed version-control wise.
        "http://www.openstreetmap.org/openlayers/OpenStreetMap.js",
        os.path.join(resources, "OpenStreetMap.js"))

finally:
    # Clean up:
    os.chdir(here)
    shutil.rmtree(tmpdir)


setuptools.setup(
    name="zc.openlayers",
    version=("%s-%s" % (VERSION, RELEASE)),
    url='http://www.zope.com',
    author='Zope Corporation',
    author_email='sales@zope.com',
    packages=['zc', 'zc.openlayers'],
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={'zc.openlayers': ['configure.zcml',
                                    'resources/Firebug/*.*',
                                    'resources/OpenLayers.js',
                                    'resources/OpenStreetMap.js',
                                    'resources/img/*',
                                    # We select *.* so img/ isn't included,
                                    # since it has to be handled separately
                                    # or distutils/setuptools chokes.
                                    'resources/theme/default/*.*',
                                    'resources/theme/default/img/*',
                                    ]},
    namespace_packages=['zc'],
    install_requires=[],
    zip_safe=False,
    )
