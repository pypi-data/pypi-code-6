from distutils.core import setup

setup(
    name='hubspot',
    version='0.1.8dev',
    packages=['hubspot',],
    license='LICENSE.txt',
    long_description=open('README.txt').read(), requires=['requests']
)
