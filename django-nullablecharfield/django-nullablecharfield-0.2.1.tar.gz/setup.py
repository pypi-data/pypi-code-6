import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-nullablecharfield',
    version='0.2.1',
    url='https://github.com/alepane21/django-nullablecharfield',
    packages=['nullablecharfield'],
    include_package_data=True,
    license='BSD License',
    description='A simple Django app that allow the use of Nullable char field.',
    long_description=README,
    author='Alessandro Pagnin',
    author_email='alepane@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
