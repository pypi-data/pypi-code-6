from distutils.core import setup

setup(
    name='flashCardStudy',
    version='1.0.4',
    author='comatory',
    author_email='osekdomains@gmail.com',
    packages=['flashcardstudy','tests','bin'],
    scripts=['bin/flashstudy.py'],
    url='https://github.com/comatory/flashCardStudy',
    license='LICENSE.txt',
    description='CLI-based utility for memorizing and studying',
    long_description=open('README.txt').read(),
	classifiers=[
				  'Programming Language :: Python',
				  'Programming Language :: Python :: 2.7',
				  'License :: OSI Approved :: MIT License',
				  'Topic :: Education',
				  ], 
	install_requires=[
		"PrettyTable",
	],
	entry_points = {
		'console_scripts': ['flashstudy = bin.flashstudy:flashcard']
			}
)
