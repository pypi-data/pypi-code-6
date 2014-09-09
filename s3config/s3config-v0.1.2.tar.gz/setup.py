from distutils.core import setup
setup(
  name = 's3config',
  packages = ['s3config'], # this must be the same as the name above
  version = '0.1.2',
  description = 'Read config file from Amazon S3 url',
  author = 'Giacomo Marinangeli',
  author_email = 'jibbolo@gmail.com',
  url = 'https://bitbucket.org/jibbolo/s3config', # use the URL to the github repo
  download_url = 'https://bitbucket.org/jibbolo/s3config/get/v0.1.tar.gz', # I'll explain this in a second
  keywords = ['config', 's3', 'aws', 'configuration','json','yaml'], # arbitrary keywords
  classifiers = [],
  install_requires=[
      'PyYAML >= 3.11',
      'boto >= 2.28.0',
      'wsgiref >= 0.1.2',
  ],
)