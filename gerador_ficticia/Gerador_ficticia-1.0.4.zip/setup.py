'''from distutils.core import setup
from cx_Freeze import setup, Executable
#para transformar em exe
# $ python setup.py build

setup(
    name='Gerador_ficticia',
    version='1.0.4',
    packages=[''],
    executables = [Executable('Projeto1.py')]
)
'''

from distutils.core import setup

setup(
	name = 'Gerador_ficticia',
	version = '1.0.4',
	py_modules = ['Projeto1'],
	author = 'Jeferson de Souza',
	author_email = 'mp_bra_nco@hotmail.com',
	description = 'Gerador de calculos de analises.',
	
)