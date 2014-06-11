from distutils.core import setup
setup(
  name = 'stelapoint',
  packages = ['stelapoint'],
  version = '0.0.1',
  description = 'Stelapoint sanctions API wrapper',
  author = 'Stelapoint',
  author_email = 'jake@stelapoint.com',
  url = 'https://github.com/stelapoint/python-sanctions-api', # use the URL to the github repo
  download_url = 'ttps://github.com/stelapoint/python-sanctions-api/tarball/0.0.2', # I'll explain this in a second
  keywords = ['stelapoint', 'sanctions', 'api'], # arbitrary keywords
  classifiers = [],
  requires=[
        "requests",
  ]
)