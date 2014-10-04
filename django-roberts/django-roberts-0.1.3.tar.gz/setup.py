import os
from setuptools import setup
from robots import __version__

setup(
    name = "django-roberts",
    version = __version__,
    author = "Mike Hurt",
    author_email = "mike@mhtechnical.net",
    description = "A simple Django app to provide access to a robots.txt file",
    license = "MIT",
    keywords = "django robots.txt",
    url = "https://bitbucket.org/mhurt/django-roberts",
    packages=['robots'],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    test_suite = 'robots._testrunner.runtests',
    tests_require=['Django >= 1.2'],
)
