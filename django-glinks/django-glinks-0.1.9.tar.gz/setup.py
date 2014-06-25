from distutils.core import setup
import os

README = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-glinks',
    version='0.1.9',
    author='Shawn Simon',
    author_email='shawn.simon.developer@gmail.com',
    packages=['glinks', "glinks.templatetags"],
    url='http://pypi.python.org/pypi/django-glinks/',
    license='LICENSE.txt (CC-BY-NC)',
    description='Interal add manager for django sites with ads not blocked by ad blocker.',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.6.0",
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)