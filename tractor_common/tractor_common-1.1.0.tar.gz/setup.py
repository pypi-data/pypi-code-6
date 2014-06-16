from setuptools import setup, find_packages

README = "Asynchronous platform for web scraping utilities'"

setup(
    name="tractor_common",
    author="Tatiana Al-Chueyr <tatiana.alchueyr@gmail.com>",
    classifiers=['Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python'],
    download_url='http://pypi.python.org/pypi/tractor_common',
    description=u"Utilities for captain-tractor project",
    include_package_data=True,
    install_requires=["requests>=2.3", "stomp.py>=3.2"],
    license="MIT License",
    long_description=README,
    packages=find_packages(),
    tests_require=["coverage>=3.6", "nose>=1.2.1", "mock>=1.0.1"],
    url="http://github.com/tatiana/captain-tractor",
    version="1.1.0"
)
