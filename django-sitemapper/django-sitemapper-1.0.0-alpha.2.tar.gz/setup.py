# Python
import os
from setuptools import setup

# Local
from sitemapper import __version__, __project__, __doc__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = [
    'Django>=1.7',
    ]

setup(
    name=__project__,
    version=__version__,
    author='Mike Hurt',
    author_email='mike@mhtechnical.net',
    description=__doc__,
    long_description=README,
    license='MIT License',
    url='https://bitbucket.org/mhurt/django-sitemapper/',
    keywords='python django sitemap.xml',
    packages=['sitemapper', 'sitemapper.migrations'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    )
