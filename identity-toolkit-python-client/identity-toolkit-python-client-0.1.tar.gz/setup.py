from distutils.core import setup
setup(
  name = 'identity-toolkit-python-client',
  packages = ['identity-toolkit-python-client'], # this must be the same as the name above
  version = '0.1',
  description = 'Google Identity Toolkit python client library',
  author = 'Jin Liu',
  #author_email = 'liujin@google.com',
  url = 'https://github.com/google/identity-toolkit-python-client', # use the URL to the github repo
  download_url = 'https://github.com/google/identity-toolkit-python-client/archive/master.zip', 
  keywords = ['identity', 'oauth2', 'login'], # arbitrary keywords
  classifiers = [],
)
