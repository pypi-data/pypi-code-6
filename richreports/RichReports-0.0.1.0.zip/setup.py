from distutils.core import setup

setup(
    name             = 'RichReports',
    version          = '0.0.1.0',
    packages         = ['richreports',],
    license          = 'MIT License',
	url              = 'http://richreports.org',
	author           = 'Chris Kuech <kuech@bu.edu>, A. Lapets <lapets@bu.edu>',
	author_email     = 'kuech@bu.edu, lapets@bu.edu',
    long_description = open('README.txt').read(),
    setup_requires   = ['uxadt'],
    install_requires = ['uxadt']
)