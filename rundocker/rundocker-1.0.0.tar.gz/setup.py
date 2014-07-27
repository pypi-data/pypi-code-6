from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
    name='rundocker',
    version='1.0.0',
    description=(
        'A script for running docker container process without worrying '
        'about dead container issue'
    ),
    packages=find_packages(),
    author='Victor Lin',
    author_email='hello@victorlin.me',
    url='https://github.com/victorlin/rundocker',
    entry_points="""\
    [console_scripts]
    rundocker = rundocker.__main__:main
    """,
)
