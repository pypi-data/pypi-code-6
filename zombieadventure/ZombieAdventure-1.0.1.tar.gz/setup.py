from setuptools import setup

setup(
	name='ZombieAdventure',
	version='1.0.1',
	author='comatory',
	author_email='osekdomains@gmail.com',
	packages=['bin','zombieadventure'],
	scripts=['bin/zombieadv.py'],
	url='https://github.com/comatory/ZombieAdventure',
	license='LICENSE.txt',
	description='Text-based survival adventure game in post-apocalyptic society.',
	long_description=open('README.txt').read(),
	entry_points={'console_scripts':['zombieadv = bin.zombieadv.py']}
	)
