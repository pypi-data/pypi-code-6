from os import path
from setuptools import setup, find_packages
from titantools import __version__ as version

README = path.join(path.dirname(__file__), 'README.md')

setup(name='titantools',
      version=version,
      description=("Support tools for Titan"),
      long_description=open('README.md').read(),
      classifiers=[
        "Programming Language :: Python",
        ("Topic :: Software Development :: Libraries :: Python Modules"),
        ],
      keywords='Titan, Mac, OSX, IDS',
      author='Mike Mackintosh',
      author_email='m@zyp.io',
      url='https://github.com/mikemackintosh/titan-tools',
      license='LICENSE.txt',
      packages=find_packages(),
      #namespace_packages=['titantools'],
)
