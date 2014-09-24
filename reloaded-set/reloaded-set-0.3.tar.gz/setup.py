from setuptools import setup, find_packages


# Dynamically calculate the version
version = __import__('reloaded_set').__version__


setup(
    name='reloaded-set',
    packages=find_packages(exclude=['tests*']),
    version=version,
    description='A frozenset that can reload his data.',
    author='',
    license="BSD",
    url='https://github.com/tomerghelber/reloaded-frozenset',
    keywords=['reloaded', 'set', ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
