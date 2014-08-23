# -*- coding: UTF-8 -*-

from distutils.core import setup
import os

README = os.path.join(os.path.dirname(__file__), 'docs/README.txt')
long_description = open(README).read()

setup(
    name='FinDt',
    version='3.0.0',
    py_modules=['findt/FinDt', 'findt/TesteFinDt'],
    author='Marcelo G Facioli',
    author_email='mgfacioli@yahoo.com.br',
    url='http://matfinanpython.blogspot.com.br/',
    keywords = ["Datas", "Calendario", "Calendario Financeiro", "Financas"],
    classifiers = [
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
		"Development Status :: 3 - Alpha",
		"Environment :: Console",
		"Intended Audience :: Financial and Insurance Industry",
		"Operating System :: OS Independent",
		"Natural Language :: Portuguese (Brazilian)",
		"Topic :: Office/Business :: Financial",
		"Topic :: Office/Business :: Financial :: Investment",
		"Topic :: Software Development :: Libraries :: Python Modules",
	],
    description='Módulo em Lingua Portuguesa contendo um conjunto de funções cujo principal objetivo é facilitar o trabalho com datas, voltadas, principalmente, para o mercado financerio do Brasil.',
    long_description = long_description,
    package_data={'':['docs/*.*']},
)