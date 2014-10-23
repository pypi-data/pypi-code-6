from distutils.core import setup
from profitshare import __version__ as VERSION

setup(name='profitshare',
      version=VERSION,
      description='ProfitShare API wrapper',
      packages=['profitshare'],
      requires=['requests'],
      author='Alex Eftimie',
      author_email='alex@eftimie.ro',
      url='https://github.com/alexef/profitshare.py',
)
