import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
readme = os.path.join(here, 'README.md')

install_requires = [
    'pytz',
    'tzlocal>=1.0.0',
]
setup_requires = [
    'coverage>=3.7.0',
    'nose>=1.3.0',
]

setup(
    name='era',
    version='1.0',
    description="Sane date and time tools for Python.",
    long_description=open(readme).read(),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: BSD License",
    ],
    keywords='date time timezone',
    author='WiFast',
    author_email='rgb@wifast.com',
    url='https://github.com/WiFast/era',
    license='BSD-derived',
    zip_safe=False,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=setup_requires,
    test_suite = 'nose.collector',
    entry_points='',
)
