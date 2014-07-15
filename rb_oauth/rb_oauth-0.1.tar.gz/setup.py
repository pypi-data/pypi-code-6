import os.path
from pkgutil import walk_packages
import sys

from reviewboard.extensions.packaging import setup

sys.path.insert(0, os.path.dirname(__file__))

import rb_oauth
from rb_oauth.extension import OAuthExtension


SUMMARY = 'This reviewboard extension allows authentication via OAuth.'
AUTHOR = 'Eric Snow'
URL = 'https://bitbucket.org/ericsnowcurrently/rb_oauth_extension'
LICENSE = 'New BSD License'


def find_packages(path, prefix=""):
    yield prefix
    prefix = prefix + "."
    for _, name, ispkg in walk_packages(path, prefix):
        if ispkg:
            yield name


def setup_reviewboard_extension(pkg, cls, summary, author, url, **kwargs):
    name = pkg.__name__
    version = pkg.__version__
    entry_point = '{} = {}:{}'.format(name, cls.__module__, cls.__name__)

    setup(
        name=name,
        version=version,
        description=summary,
        author=author,
        url=url,
        packages=list(find_packages(rb_oauth.__path__, name)),
        entry_points={'reviewboard.extensions': entry_point},
        package_data={name: ['templates/*.html']},
        **kwargs
    )


setup_reviewboard_extension(pkg=rb_oauth,
                            cls=OAuthExtension,
                            summary=SUMMARY,
                            author=AUTHOR,
                            url=URL,
                            license=LICENSE,
                            )
