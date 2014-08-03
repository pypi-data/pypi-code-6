from distutils.core import setup
from os.path import join

setup(
    name="GameBaker",
    version="0.1dev",
    packages=["gamebaker",],
    author="Roderick MacSween",
    author_email='roddylm2@gmail.com',
    license="LICENSE.txt",
    url="https://github.com/sweeneyrod/game-baker",
    long_description=open('README.txt').read(),
    scripts=[join("bin", "newproject.py"),
             join("bin", "exampleproject.py"),],
)