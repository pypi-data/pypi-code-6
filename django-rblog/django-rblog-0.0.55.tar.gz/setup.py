# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='django-rblog',
    version='0.0.55',
    author=u'Oscar M. Lage Guitian',
    author_email='r0sk10@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    url='http://bitbucket.org/r0sk/django-rblog',
    license='BSD licence, see LICENSE file',
    description='Yet another Django Blog App',
    zip_safe=False,
    long_description=open('README.rst').read(),
    install_requires=[
        "Django < 1.5",
        "Pygments",
        "BeautifulSoup",
        "South == 0.8.1",
        "PIL == 1.1.7",
        "django-tinymce >= 1.5.1",
        "django-filebrowser-no-grappelli == 3.1.1",
        "django-tagging == 0.3.1",
        "django-compressor == 1.3",
        "sorl-thumbnail == 11.12",
        "elementtree==1.2.7-20070827-preview",
        "disqus-python==0.4.2",
        "django-disqus==0.4.1",
    ],
    keywords = "django application blog",
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
