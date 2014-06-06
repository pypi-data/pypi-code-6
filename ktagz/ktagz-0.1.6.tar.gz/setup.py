from setuptools import setup
from setuptools import find_packages

setup(
	name = "ktagz",
	packages = find_packages(),
	version = "0.1.6",
	description = "A command line file-tagger/file-search tool for linux",
	long_description = open('README.md').read(),
	author = "Khirod Kant Naik",
	author_email = "khirod234@gmail.com",
	url='https://github.com/shinigamiryuk/TagZ',
	scripts = ['bin/ktagz'],
)
