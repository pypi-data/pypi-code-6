import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme_file:
    README = readme_file.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-silk',
    version='0.2.2',
    packages=['silk'],
    include_package_data=True,
    license='MIT License',
    description='A Django app for profiling other Django apps',
    long_description=README,
    url='http://www.mtford.co.uk/projects/silk/',
    author='Michael Ford',
    author_email='mtford@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires= [
        'Django>=1.5,<1.7',
        'Pygments==1.6',
        'six==1.6',
        'simplejson>=3,<4',
        'python-dateutil>=2,<3',
        'requests>=2,<=3',
        'sqlparse>=0.1,<0.2',
        'Jinja2>=2.7,<3',
        'autopep8>=1,<2'
    ]
)
