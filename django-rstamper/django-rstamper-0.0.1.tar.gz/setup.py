# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='django-rstamper',
    version='0.0.1',
    author=u'Oscar M. Lage Guitian',
    author_email='r0sk10@gmail.com',
    #packages=['rstamper'],
    packages = find_packages(),
    include_package_data = True,
    package_data = {'': ['rstamper/templates', 'rstamper/static','rstamper/fixtures',], 'rstamper-example': ['rstamper-example/*']},
    url='http://bitbucket.org/r0sk/django-rstamper',
    license='BSD licence, see LICENSE file',
    description='Yet another Django Gallery App',
    zip_safe=False,
    long_description=open('README.rst').read(),
    install_requires=[
        "Django < 1.5",
        "South == 0.7.5",
    ],
    keywords = "django application stamper",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
