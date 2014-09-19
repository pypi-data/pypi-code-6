from setuptools import setup

setup(name='melange_downloader',
		version='0.3',
		description='Download testimonials in a sorted way from BITS Melange website.',
		url='http://github.com/bhavul/testimonials-downloader',
		author='Bhavul Gauri',
		author_email='bhavul93@gmail.com',
		license='MIT',
		packages=['melange_downloader'],
		install_requires=['BeautifulSoup',],
		zip_safe=False)