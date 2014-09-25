from distutils.core import setup

setup(name='asyncoro',
      version='3.0.2',
      description='Python framework for concurrent, distributed, asynchronous network programming with coroutines, asynchronous completions and message passing.',
      url='http://asyncoro.sourceforge.net',
      py_modules=['asyncoro', 'asyncoro3', 'disasyncoro', 'disasyncoro3', 'asyncfile', 'asyncfile3', 'discoro'],
      scripts=['discoro.py'],
      author='Giridhar Pemmasani',
      author_email='pgiri@yahoo.com',
      license='The MIT License: http://opensource.org/licenses/MIT',
      platforms='any',
      classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Topic :: Scientific/Engineering',
          'Topic :: Software Development', ]
      )
