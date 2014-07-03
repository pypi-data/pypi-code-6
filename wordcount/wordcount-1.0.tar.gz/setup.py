from setuptools import setup, find_packages

setup(
	name = "wordcount",
	version = '1.0',
	description = "Count the Number of Words in a File",
	author = "Sarvagya Pant",
	author_email = "sarvagya.pant@gmail.com",
	url = "www.pantsarvagya.com.np",
	packages=find_packages(exclude=['ez_setup']),
	entry_points={
        'console_scripts': [
            'wordcount = wordcount.wordcount:main'
        ]
    }

)