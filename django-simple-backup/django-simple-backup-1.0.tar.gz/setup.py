import ez_setup
ez_setup.use_setuptools()
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-simple-backup',
    version     = '1.0',
    author        = 'Evgeny Fadeev',
    author_email = 'evgeny.fadeev@gmail.com',
    url            = '',
    description    = 'A simple backup command for Django',
    packages=find_packages(),
    include_package_data=True,
)

