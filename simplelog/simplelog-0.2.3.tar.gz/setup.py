from distutils.core import setup

PACKAGE = "simplelog"
NAME = "simplelog"
DESCRIPTION = "Simple logging interface for python"
AUTHOR = "Kevin S  Lin"
AUTHOR_EMAIL = "kevinslin8@gmail.com"
URL = ""
VERSION = __import__(PACKAGE).__version__


setup(name = 'simplelog',
      version = VERSION,
      description = 'Simple interface for logging in python',
      author = 'Kevin S Lin',
      author_email = 'kevinslin8@gmail.com',
      url = 'kevinslin.com',
      long_description = DESCRIPTION,
      packages = ['simplelog']
      )
