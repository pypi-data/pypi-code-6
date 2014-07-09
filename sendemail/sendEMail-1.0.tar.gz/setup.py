from distutils.core import setup
import sendEMail as module

setup(name='sendEMail',
	description='Simple way to send Email from dico.',
	version='1.0',
	scripts= ['sendEMail.py'],
	url='https://github.com/Mrletejhon/sendMail.git',
	download_url = 'https://github.com/Mrletejhon/sendMail/tarball/0.1',
	py_modules=['sendEMail']
	)