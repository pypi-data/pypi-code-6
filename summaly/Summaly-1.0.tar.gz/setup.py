from distutils.core import setup

setup(
	name = 'Summaly',
	version = '1.0',
	author = 'Sagar Pandey',
	author_email = 'sagarinocean@gmail.com',
	packages = ['summary_wiki'],
	scripts = [],
	url = 'https://pypi.python.org/pypi/summaly/',
	license = 'LICENSE.txt',
	description = 'Summarizes a Wikipedia Document',
	long_description = open('README.txt').read(),
	install_requires = ["nltk == 3.0.0b1","beautifulsoup4 == 4.3.2","bleach == 1.4","requests == 2.2.1",],

	)
