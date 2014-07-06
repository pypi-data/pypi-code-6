from distutils.core import setup

setup(
    name='Mirador',
    version='0.1.1',
    author='Nick Jacob - Mirador',
    author_email='nick@mirador.im',
    packages=['mirador', 'mirador.test', 'mirador.ext'],
    scripts=['bin/mirador-client'],
    url='http://github.com/mirador-cv/mirador-py',
    license='LICENSE.txt',
    description='client for the Mirador image moderation API. (mirador.im)',
    install_requires=[
        "requests >= 2.3.0"
    ],
)
