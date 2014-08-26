from setuptools import setup, find_packages

exec(open('fanery/_version.py'))
setup(
    name='Fanery',
    version=__version__, # noqa
    author='Marco Caramma',
    author_email='marco@globalsoftwaresecurity.com',
    url='https://pypi.python.org/pypi/Fanery/',
    license='ISC',
    description='Application development framework',
    long_description=open('README.txt').read(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'msgpack-python',
        'python-libuuid',
        'ciso8601',
        'bsdiff4',
        'PyNaCl',
        'scrypt',
        'ujson',
        'cxor',
        'webob',
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: BSD',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: Session',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
