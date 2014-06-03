"""
Biomedical Genomics Python core libraries
"""

from setuptools import setup, find_packages

from bgcore import VERSION, AUTHORS, CONTACT_EMAIL

setup(
	name = "bgcore",
	version = VERSION,
	packages = find_packages(),

	# metadata
	author = AUTHORS,
	author_email = CONTACT_EMAIL,
	description = "Biomedical Genomics Python core libraries",
	license = "UPF Free Source Code",
	keywords = "",
	url = "https://bitbucket.org/bbglab/bgcore",
	download_url = "https://bitbucket.org/bbglab/bgcore/get/0.4.0.tar.gz",
	long_description = __doc__,

	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: Other/Proprietary License",
		"Environment :: Console",
		"Intended Audience :: Science/Research",
		"Natural Language :: English",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Topic :: Scientific/Engineering",
		"Topic :: Scientific/Engineering :: Bio-Informatics"
	]
)
