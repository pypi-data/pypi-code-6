import os
from setuptools import setup, find_packages
import pyramid_turbolinks

here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.md')) as f:
        README = f.read()
except IOError:
    README = pyramid_turbolinks.__doc__

try:
    VERSION = pyramid_turbolinks.__version__
except AttributeError:
    VERSION = '1.0'

try:
    REQUIREMENTS = pyramid_turbolinks.__depends__
except AttributeError:
    REQUIREMENTS = []

setup(
    name = 'pyramid_turbolinks',
    version = VERSION,
    author = 'Eric Hulser',
    author_email = 'eric.hulser@projexsoftware.com',
    maintainer = 'Projex Software',
    maintainer_email = 'team@projexsoftware.com',
    description = '''''',
    license = 'LGPL',
    keywords = '',
    url = 'http://www.projexsoftware.com',
    include_package_data=True,
    packages = find_packages(),
    install_requires = REQUIREMENTS,
    tests_require = REQUIREMENTS,
    long_description= README,
    classifiers=[],
)