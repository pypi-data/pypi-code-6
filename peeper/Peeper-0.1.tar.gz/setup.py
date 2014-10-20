# peeper - setup.py
from distutils.core import setup

setup(
	name = "Peeper",
	packages = ['peeper'],
	scripts=['bin/peeper.py'],
	version = "0.1",
	license = "BSD License",
	description = "Peep inside a Python sdist tarball/zip and find its dirty requirements.",
	author = "Roland Shoemaker",
	author_email = "rolandshoemaker@gmail.com",
	url = "https://github.com/rolandshoemaker/py-peeper",
	download_url = "https://github.com/rolandshoemaker/py-peeper/tarball/v0.1",
	keywords = ["pypi", "sdist", "requires", "requirements"],
	classifiers = ["Programming Language :: Python",
	"Programming Language :: Python :: 2",
	"Development Status :: 4 - Beta",
	"Environment :: Console",
	"Intended Audience :: Developers",
	"License :: OSI Approved :: BSD License",
	"Operating System :: OS Independent",
	"Topic :: System :: Archiving :: Packaging",
	"Topic :: System :: Software Distribution",
	"Topic :: Utilities"])
