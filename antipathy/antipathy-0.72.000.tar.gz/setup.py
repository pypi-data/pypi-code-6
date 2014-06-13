from distutils.core import setup
import os


long_desc="""\
Antipathy -- for those tired of ``os.path``
===========================================

Tired of calling a function for every path manipulation you need to do?

Is::

    >>> path, filename = os.path.split(some_name)
    >>> basename, ext = os.path.splitext(filename)
    >>> basename = basename + '_01'
    >>> new_name = os.path.join([path, basename, ext])

wearing on your nerves?

In short, are you filled with antipathy [1] for os.path?

Then get antipathy and work with Path::

    >>> some_name = Path('/home/ethan/source/my_file.txt')
    >>> backups = Path('/home/ethan/backup/')
    >>> print some_name.path
    '/home/ethan/source/'
    >>> print some_name.ext
    '.txt'
    >>> print some_name.exists()
    True  # (well, if it happens to exist at this moment ;)
    >>> backup = backups / some_name.filename + '_01' + some_name.ext
    >>> print backup
    '/home/ethan/backup/my_file_01.txt'
    >>> some_name.copy(backup)

Because Path is a subclass of str/unicode, it can still be passed to other functions that expect a str/unicode object and work seamlessly.

[1] https://www.google.com/#q=antipathy
"""

setup( name='antipathy',
       version= '0.72.000',
       license='BSD License',
       description='oo view of file paths and names, subclassed from str/unicode',
       long_description=long_desc,
       url='http://groups.google.com/group/python-dbase',
       py_modules=['path', 'path_test'],
       provides=['path'],
       author='Ethan Furman',
       author_email='ethan@stoneleaf.us',
       classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python',
            'Topic :: Database',
            'Programming Language :: Python :: 2.4',
            'Programming Language :: Python :: 2.5',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            ],
    )

