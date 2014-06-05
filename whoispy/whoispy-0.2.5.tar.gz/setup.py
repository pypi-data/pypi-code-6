from distutils.core import setup


setup( name = "whoispy",
	version = "0.2.5",
	license = "GPL License",
	package_dir={'whoispy': 'whoispy'},
	packages=['whoispy'],
	description = "Python module/library to get the WHOIS information",
	author = "nemunemu",
	author_email = "oss@nemumu.com",
	url = "https://github.com/nemumu/whoispy",
	keywords = ["whois", "network", "domain", "jpnic"],
	
	classifiers = [
		'Environment :: Console',
		'Environment :: Web Environment',
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: Developers',
		'Intended Audience :: System Administrators',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python',
		'Topic :: Communications :: Email',
	],

	long_description = """
This module supports .aero .arpa .asia 
.biz .cat .com .coop .edu .gov .info .int
.jobs .mobi .museum .name .net .org .pro
.tel .travel domain.
I'm looking for pull requests!
	"""
)
