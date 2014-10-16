from setuptools import setup

import ucnum

setup(
	name=ucnum.__name__,
	version=ucnum.__version__,
	author='Philipp A.',
	author_email='flying-sheep@web.de',
	description='Unicode helper and search utility',
	license='GPL',
	keywords='unicode',
	url='http://github.com/flying-sheep/ucnum',
	py_modules=['ucnum'],
	scripts=['ucnum'],
	long_description=ucnum.__doc__,
	install_requires=['unicodeblocks'],
	classifiers=[
		'Topic :: Utilities',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Development Status :: 5 - Production/Stable',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
	],
)