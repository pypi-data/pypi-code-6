import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()


setup(
    name='mrrapi',
    version='0.3',
    url='https://github.com/jcwoltz/mrrapi',
    description='MinigRigRentals.com python API integration',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Topic :: Office/Business :: Financial"
    ],
    author='jcwoltz',
    author_email='jwoltz@gmail.com',
    keywords='mrr miningrigrentals api bitcoin',
    packages=['mrrapi'],
    install_requires=['requests'],
    include_package_data=True,
    zip_safe=False,
    test_suite="mrrapi",
)
