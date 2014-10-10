from setuptools import setup, find_packages

version = '0.7'

setup(
    name='pyjon.utils',
    version=version,
    description="Useful tools library with classes to do singletons, dynamic function pointers...",
    long_description=open("README.rst").read(),
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='Florent Aide',
    author_email='florent.aide@gmail.com',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['pyjon'],
    include_package_data=True,
    zip_safe=False,
    tests_require=['nose', 'nosexcover'],
    test_suite='nose.collector',
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
