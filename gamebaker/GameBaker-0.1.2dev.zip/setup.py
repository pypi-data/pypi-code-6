from distutils.core import setup
from os.path import join

setup(
    name="GameBaker",
    version="0.1.2dev",
    description="High level framework for making games based on Pygame",
    packages=["gamebaker",],
    author="Roderick MacSween",
    author_email='macsweenroddy@gmail.com',
    license=open("LICENSE.txt").read(),
    long_description=open('README.txt').read(),
    scripts=[join("bin", "newproject.py"),
             join("bin", "exampleproject.py"),],
)