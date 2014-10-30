from setuptools import setup, find_packages

setup(
    name = 'quaidan',
    version = '0.2.1',
    packages = find_packages(),
    url = 'http://github.com/stefanbirkner/quaidan/',
    download_url = 'https://github.com/stefanbirkner/quaidan/archive/quaidan-0.2.1.tar.gz',
    license = 'MIT License',
    install_requires = ['lxml', 'requests'],
    tests_require = ['PyHamcrest>=1.0'],
    description = 'Quaidan is a python wrapper for mod_proxy_balancer\'s balancer manager.',
    author = 'Stefan Birkner',
    author_email = 'mail@stefan-birkner.de',
    platforms = 'any',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration'
        ],
    test_suite = "tests"
)
