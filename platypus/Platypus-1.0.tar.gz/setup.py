from setuptools import setup, find_packages
from platypus._version import __version__

setup(name='Platypus',
    version=__version__,
    description='A minimal language',
    url='http://github.com/anayjoshi/platypus',
    author='Anaykumar Joshi',
    author_email='anaykumar.joshi@gmail.com',
    license='BSD',
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        'ply',
    ],
    entry_points="""
    [console_scripts]
    platypus=platypus.shell:run
    """,
    scripts=[
    ],
    zip_safe=False)
