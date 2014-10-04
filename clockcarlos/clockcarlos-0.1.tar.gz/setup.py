from setuptools import setup

def readme():
	with open('README.rst') as f:
		return f.read()

setup(	name = 'clockcarlos',
		version = '0.1',
		description = 'so you can have a visible timer on your terminal',
		long_description = 'The same as the short descript',
		classifiers = [
			'Development Status :: 3 - Alpha',
			'License :: OSI Approved :: MIT License',
			'Programming Language :: Python :: 2.7'],
		keywords = 'clock carlos timer hiphop iggy azalea white chicks',
		url = 'www.google.com',
		author = 'TheTempest',
		author_email = 'thetempest@gmail.com',
		license = 'MIT',
		packages = ['clockcarlos'],
		zip_safe = False)