from __future__ import unicode_literals

import os as _os


__version__ = '0.2.1'


# TO use run:
# travis encrypt 'PYPI_PASSWORD=adsfasdfasdf' --add

config = dict(
    PYPI_USERNAME='omnibus',
    PYPI_PASSWORD=None,
    PYPI_INDEX='https://pypi.vandelay.io/balanced/prod/',
    PUBLISH_BRANCH='master'
)


for k in config:
    config[k] = _os.environ.get(k, config[k])
