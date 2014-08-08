from distutils.core import setup
setup(
  name = 'permalink_adder',
  packages = ['permalink_adder'], # this must be the same as the name above
  version = '0.1',
  description = 'SEO tool for adding permalinks to text contained in Django apps databases.',
  author = 'Piotr Lizonczyk',
  author_email = 'piotr.lizonczyk@gmail.com',
  url = 'https://github.com/plizonczyk/permalink_adder', # use the URL to the github repo
  download_url = 'https://github.com/plizonczyk/permalink_adder/tarball/0.1', # I'll explain this in a second
  keywords = ['SEO', 'permalinks'], # arbitrary keywords
  classifiers = ['Development Status :: 2 - Pre-Alpha',
                 'Framework :: Django',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 2.7'],
)