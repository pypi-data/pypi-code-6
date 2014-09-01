# coding: utf-8
from setuptools import setup

setup(
    name='github_list_issues',
    version="0.1.0",
    description='List all issues assigned to the user on GitHub',
    author=u'Matěj Cepl',
    author_email='mcepl@cepl.eu',
    url='https://github.com/mcepl/github_list_issues',
    scripts=['github_list_issues'],
    keywords=['github', 'issues', 'developer'],
    install_requires=['urllib2_prior_auth'],
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
