"""dummy_test - Dummy test package for testing purposes

This package is super small and light used for pip testing purposes

"""

classifiers = """\
Development Status :: 5 - Production/Stable
Environment :: Console
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python :: 2
Topic :: Software Development :: Quality Assurance
Topic :: Software Development :: Testing
""".splitlines()

from setuptools import setup

doc = __doc__.splitlines()

setup(
    name="dummy_test",
    version="0.1.1",
    packages=['dummy_test'],
    zip_safe=False,
    author='Kien Pham',
    author_email='kien@sendgrid.com',
    url="https://github.com/kienpham2000/dummy_test",
    license='MIT',
    description=doc[0],
    long_description='\n'.join(doc[2:]),
    keywords='dummy test',
    classifiers=classifiers
)