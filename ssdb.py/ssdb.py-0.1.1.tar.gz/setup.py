"""
ssdb.py
-------

Ssdb Python Client Library.

Sample
``````

.. code:: python

    >>> from ssdb import SSDBClient
    >>> c = SSDBClient(host='localhost', port=8888)
    >>> c.set('key', 'val')
    1
    >>> c.get('key')
    'val'

Source
``````

https://github.com/hit9/ssdb.py
"""

from setuptools import setup


setup(
    name='ssdb.py',
    version='0.1.1',
    author='hit9',
    author_email='nz2324@126.com',
    description="Ssdb Python Client Library",
    long_description=__doc__,
    license='bsd2',
    keywords=['ssdb', 'client', 'library'],
    url='https://github.com/hit9/ssdb.py',
    py_modules=['ssdb'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
