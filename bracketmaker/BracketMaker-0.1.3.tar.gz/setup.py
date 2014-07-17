from distutils.core import setup

setup(
    name='BracketMaker',
    version='0.1.3',
    author='Dylan Richardson',
    author_email='bigdrich14@gmail.com',
    packages=['bracket'],
    scripts=['bin/main.py'],
    url='http://pypi.python.org/pypi/BracketMaker/',
    license='LICENSE.txt',
    description='Create and store readable brackets.',
    long_description=open('README.txt').read(),
    install_requires=[],
)