from distutils.core import setup

setup(
    name='ZombieAdventure',
    version='1.0.0',
    author='comatory',
    author_email='osekdomains@gmail.com',
    packages=['bin','zombieadventure'],
    scripts=['bin/zombieadv.py'],
    url='https://github.com/comatory/ZombieAdventure',
    license='LICENSE.txt',
    description='Adventure Game',
    long_description=open('README.txt').read(),
    classifiers=[
                  ], 
    install_requires=[
        
    ],
    entry_points = {
        'console_scripts': ['zombieadv = bin.zombieadv:main']
            }
)
