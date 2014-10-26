#http://docs.activestate.com/activepython/3.2/diveintopython3/html/packaging.html

from distutils.core import setup

setup(
   name = 'xmlComparator',
   url = 'http://pypi.python.org/pypi/xmlComparator',
   packages = ['xmlComparison'],
   #py_modules = [],
   scripts = ['xmlComparator'],
   version = '1.0.2',
   description = 'xml comparison ignoring order of child nodes',
   author = 'Chun Shang',
   author_email = 'shangchun262@163.com',
   classifiers = ['Programming Language :: Python',
                  'Programming Language :: Python :: 3',
                  'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                  'Operating System :: OS Independent',
                  'Intended Audience :: Developers',
                  'Topic :: Text Processing :: Markup :: XML'
                  ]
)
