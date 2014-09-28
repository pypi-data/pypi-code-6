import os
from setuptools import setup
from qanda import __version__

setup(
    name = "django-qanda",
    version = __version__,
    author = "Mike Hurt",
    author_email = "mike@mhtechnical.net",
    description = "A simple FAQ app for Django sites.",
    license = "MIT",
    keywords = "faq question answer django",
    url = "https://bitbucket.org/mhurt/qanda",
    packages=['qanda'],
    test_suite = 'runtests.main',
    tests_require=['Django'],
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
