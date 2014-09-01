from distutils.core import setup
from cx_Freeze import setup, Executable
#para transformar em exe
# $ python setup.py build

setup(
    name='Gerador_ficticia',
    version='1.0.1',
    packages=[''],
    executables = [Executable('Projeto1.py')]
)
