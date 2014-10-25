from setuptools import setup
from mgmarkdown import __version__

setup(
    name='mgmarkdown',
    version=__version__,
    description='Markdown converter with personal extensions',
    author='Michael Goerz',
    author_email='mail@michaelgoerz.net',
    url='https://github.com/goerz/mgmarkdown',
    license='GPL',
    packages=['mgmarkdown'],
    entry_points={
    'console_scripts': ['mgmarkdown = mgmarkdown:main', ],},
)
