from setuptools import setup, find_packages

setup(
    name="cuaffils",
    version="1.0.0",
    author="Anders Pearson",
    author_email="anders@columbia.edu",
    url="",
    description="CU affil strings",
    long_description="generate and parse various formats",
    install_requires = [],
    scripts = [],
    license = "BSD",
    platforms = ["any"],
    zip_safe=False,
    package_data = {'' : ['*.*']},
    packages=['cuaffils'],
    test_suite='cuaffils.tests',
    )
