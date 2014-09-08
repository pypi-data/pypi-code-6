from codecs import open
from os import path

from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lribeiro.cherrypy.templating',
    version='1.0',
    description='Template rendering tool for cherrypy',
    long_description=long_description,
    url='http://bitbucket.org/livioribeiro/cherrypy-templating',
    author='Livio Ribeiro',
    author_email='livioribeiro@outlook.com',
    license='BSD License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: CherryPy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords=['templating', 'cherrypy', 'mako', 'jinja2', 'pystache', 'cheetah', 'genshi'],
    namespace_packages=['lribeiro', 'lribeiro.cherrypy'],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'CherryPy',
    ]
)