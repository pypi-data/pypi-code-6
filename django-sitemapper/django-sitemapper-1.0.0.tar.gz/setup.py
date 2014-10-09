# Python
import os
from setuptools import setup

# Local
from sitemapper import __version__, __project__, __doc__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name=__project__,
    version=__version__,
    author='Mike Hurt',
    author_email='mike@mhtechnical.net',
    description=__doc__,
    long_description=README,
    license='MIT License',
    url='https://bitbucket.org/mhurt/django-sitemapper/',
    install_requires=['Django >= 1.4.2'],
    keywords='python django sitemap.xml',
    packages=['sitemapper', 'sitemapper.migrations', 'sitemapper.tests'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    test_suite='sitemapper.tests.run.runtests',
    tests_require=[
        'django-discover-runner',
        'Django >= 1.4.2',
        ],
    )
