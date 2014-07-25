import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name = "cdn-fastly",
	version = "1.0.4",
	author = "Obulapathi N Challa",
	author_email = "obulpathi@gmail.com",
	description = ("A Python client libary for the Fastly API."),
	license = "BSD",
	keywords = "fastly",
	url = "https://github.com/obulpathi/cdn-fastly-python",
	packages=['fastly', 'tests'],
	scripts=['bin/fastly_upload_vcl.py', 'bin/fastly_purge_url.py'],
	long_description=read('README'),
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"License :: OSI Approved :: BSD License",
	],
)
