from os.path import abspath, dirname, join
try:
  # try to use setuptools
  from setuptools import setup
  setupArgs = dict(
      include_package_data=True,
      namespace_packages=['dm', 'dm.zope'],
      install_requires=[
        "dm.zopepatches.ztutils",
        "decorator",
        # "notmuch", # not included explicitely, to facilitate use of the OS level `python-notmuch` package
        "five.formlib",
        "zope.formlib",
      ],
      zip_safe=False,
      )
except ImportError:
  # use distutils
  from distutils import setup
  setupArgs = dict(
    )

cd = abspath(dirname(__file__))
pd = join(cd, 'dm', 'zope', 'notmuchmail')

def pread(filename, base=pd): return open(join(base, filename)).read().rstrip()

setup(name='dm.zope.notmuchmail',
      version=pread('VERSION.txt').split('\n')[0],
      description="Zope interface to the email indexer and retriever `notmuch[mail]`",
      long_description=pread('README.txt'),
      classifiers=[
        'Development Status :: 4 - Beta',
 #       'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        "Intended Audience :: System Administrators",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
        'Framework :: Zope2',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        "Topic :: Communications :: Email",
        ],
      author='Dieter Maurer',
      author_email='dieter@handshake.de',
      url='http://pypi.python.org/pypi/dm.zope.notmuchmail',
      packages=['dm', 'dm.zope', 'dm.zope.notmuchmail'],
      keywords='email retrieval zope notmuchmail notmuch',
      license='BSD',
      **setupArgs
      )
