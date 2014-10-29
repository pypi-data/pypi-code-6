import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'django-theming',
    version = '0.1',
    packages = [
        'theming',
        'theming.management',
        'theming.management.commands',
        'theming.templatetags'
    ],
    include_package_data = True,
    description = 'Django app to implement the concept of theming, allow theming for host url.',
    long_description = README,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)