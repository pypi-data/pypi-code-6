from distutils.core import setup

setup( name = "getvps",
	version = "0.0.1",
	py_modules = ["getvps"],
	license = "GPL License",
	description = "Python module/library to get Free VPS.",
	author = "nemunemu",
	author_email = "oss@nemumu.com",
	url = "https://github.com/nemumu/getvps",
	keywords = ["getvps", "vps", "server", "free"],
	
	install_requires=[
		'requests',
	],

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
This module uses the FreeServer.
I'm looking for pull requests!
	"""
)
