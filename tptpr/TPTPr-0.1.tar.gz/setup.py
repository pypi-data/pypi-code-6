try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup
	
config = {
	'description': 'T. Pelz Test Project - TPTP',
	'author': 'T. Pelz',
	'url': 'No URL',
	'download_url': 'Github?',
	'author_email': 'tapelz@gmail.com',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['TPTP'],
	'scripts': ['bin/testscript.py'],
	'name': 'TPTPr'
	}
	
setup(**config)
