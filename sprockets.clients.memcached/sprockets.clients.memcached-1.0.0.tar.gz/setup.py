import codecs
import sys

import setuptools

install_requires = ['sprockets']

if sys.version_info < (3, 0):
    install_requires.append('python-memcached')
if sys.version_info >= (3, 0):
    install_requires.append('python3-memcached')


setuptools.setup(
    name='sprockets.clients.memcached',
    version='1.0.0',
    description=('Memcached client wrapper that is configured via '
                 'environment variables'),
    long_description=codecs.open('README.rst', encoding='utf-8').read(),
    url='https://github.com/sprockets/sprockets.clients.memcached.git',
    author='AWeber Communications',
    author_email='api@aweber.com',
    license=codecs.open('LICENSE', encoding='utf-8').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=['sprockets',
              'sprockets.clients',
              'sprockets.clients.memcached'],
    package_data={'': ['LICENSE', 'README.rst']},
    include_package_data=True,
    namespace_packages=['sprockets',
                        'sprockets.clients'],
    install_requires=install_requires,
    zip_safe=False)
