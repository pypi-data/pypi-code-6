import bidict
from setuptools import setup

setup(
    name='bidict',
    version='0.1.5',
    author='Josh Bronson',
    author_email='jabronson@gmail.com',
    description="2-way dict with convenient slice syntax: d[65] = 'A' -> d[:'A'] == 65",
    long_description=bidict.__doc__,
    keywords='bidirectional, two-way, inverse, reverse, dict, dictionary, mapping',
    url='https://bitbucket.org/jab/bidict',
    license='MIT',
    py_modules=['bidict'],
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: English',
        ],
    )
