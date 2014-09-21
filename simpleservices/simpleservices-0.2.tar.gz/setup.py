import sys
if sys.argv[1] == 'develop':
    from setuptools import setup
else:
    from distutils.core import setup
__version__ = (0,2)
setup(
    name='simpleservices',
    version='.'.join([str(x) for x in __version__]),
    author='Hugo Shi',
    author_email='hugo.r.shi@gmail.com',
    description='utility for running simple services',
    packages=['simpleservices'],
    include_package_data=True,
    url='http://github.com/hhuuggoo/simpleservices',
    package_data={'simpleservices':['*.conf']}
)
