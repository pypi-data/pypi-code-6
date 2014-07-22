#
import glob
import os
import re

try:
    import setuptools
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()

from setuptools import setup, Extension, find_packages


VERRX = re.compile(r'((\d+\.)+\d)\.txt$')

def versionFromReleaseNotes():
    """
    Hypy's official version is the latest version of the release notes found
    in doc/release-notes.
    """
    thisDir = os.path.abspath(__file__).rsplit(os.sep, 1)[0]
    if thisDir == __file__:
        thisDir = ''

    versions = glob.glob(os.sep.join(
        [thisDir, 'doc', 'release-notes', '[0-9]*.txt']))
    if versions:
        return VERRX.search(max(versions)).group(1)
    else:
        return 'VERSION_NOT_FOUND'


ext = Extension("_estraiernative",
                ["estraiernative.c"],
                libraries=["estraier"],
                include_dirs=["/usr/include/estraier", "/usr/include/qdbm"],
                )

setup(
        name="Hypy", 
        description='Pythonic wrapper for Hyper Estraier',
        author='Yusuke YOSHIDA',
        author_email='usk@nrgate.jp',
        maintainer='Cory Dodt',
        maintainer_email='pypi@spam.goonmill.org',
        url='http://goonmill.org/hypy/',
        download_url='http://hypy-source.goonmill.org/archive/tip.tar.gz',
        version=versionFromReleaseNotes(),
        ext_modules=[ext],
        zip_safe=False,
        packages=find_packages(),

        install_requires=[
            'Distribute>=0.6.3',
            ],

        classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries',
          'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
          ],
      )
