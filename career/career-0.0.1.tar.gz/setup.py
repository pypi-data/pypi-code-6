from setuptools import setup, find_packages
from career import __version__ as version

with open('README.rst') as f:
    long_description = f.read()

setup(
    name = 'career',
    version = version,
    description = 'The very basic to start some elearning activity',
    long_description = long_description,
    author = 'Daniel Tellez',
    author_email = 'danieltellez@flossfriday.com',
    url = 'https://github.com/danieltellez/career',
    packages = find_packages(
        exclude = [
            'testproject',
            'testproject.app',
        ],
    ),
    zip_safe=False,
    include_package_data = True,
    install_requires=[
        'Django>=1.3',
        'django-hvad',
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Education",
    ]
)


