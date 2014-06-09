from distutils.core import setup

setup(
    name='hubspot',
    version='0.1.9dev',
    packages=['hubspot',],
    license='LICENSE.txt',
    long_description=open('README.txt').read(), requires=['requests']
)
