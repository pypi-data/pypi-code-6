# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

PACKAGE = "django_smtp_alternative"
NAME = "django-smtp-alternative"
DESCRIPTION = "Django email backend providing sending with alternative SMTP server if primary server fails"
AUTHOR = "Jan Češpivo, COEX CZ s.r.o (http://www.coex.cz)"
AUTHOR_EMAIL = "jan.cespivo@gmail.com"
URL = "https://github.com/COEXCZ/django-smtp-alternative"
VERSION = '1.0.0'
LICENSE = "LGPLv3"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    url=URL,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    install_requires=[
        "django",
    ],
)
