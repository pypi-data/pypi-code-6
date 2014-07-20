try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'Rock Paper Scissor',
	'author' : 'Mridu Bhattacharya',
	'author_email' : 'mridubhattacharya@live.com',
	'version' : '0.1',
	'install_requires' : ['nose'],
	'packages' : ['rockpaperscissor'],
	'name' : 'rockpaperscissor',
	'url' : 'https://pypi.python.org/pypi'
}

setup(**config)