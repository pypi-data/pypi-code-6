from setuptools import setup
setup(
  name = 'overlord',
  packages = [''], 
  version = '0.1',
  description = "Seattle's overlord package",
  author = 'Seattle',
  url = 'https://github.com/BuildSeash/overlord', # use the URL to the github repo
  download_url = 'https://github.com/BuildSeash/overlord/tarball/0.1',
  install_requires = ['seash', 'repy_v2', 'clearinghouse', 'portability'],
  dependency_links = ["https://github.com/BuildSeash/seash/tarball/0.1" 
  ],
  classifiers = []
)