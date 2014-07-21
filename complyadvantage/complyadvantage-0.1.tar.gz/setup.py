from distutils.core import setup
setup(
  name = 'complyadvantage',
  packages = ['complyadvantage'],
  version = '0.1',
  description = 'ComplyAdvantage sanctions API wrapper',
  author = 'ComplyAdvantage',
  author_email = 'jake@complyadvantage.com',
  url = 'https://github.com/complyadvantage/python-sanctions-api', # use the URL to the github repo
  download_url = 'https://github.com/complyadvantage/python-sanctions-api/tarball/0.1', # I'll explain this in a second
  keywords = ['complyadvantage', 'sanctions', 'api'], # arbitrary keywords
  classifiers = [],
  requires=[
        "requests",
  ]
)