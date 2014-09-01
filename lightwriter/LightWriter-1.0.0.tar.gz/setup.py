from setuptools import setup, find_packages

setup(
    name='LightWriter',
    version='1.0.0',
    author='Mike Kadin',
    author_email='michaelkadin@gmail.com',
    packages=find_packages(),
    scripts=['bin/example.py'],
    url='http://pypi.python.org/pypi/LightWriter/',
    license='LICENSE.txt',
    description='Control a RadioShack Light Strip with an Arduino and Python',
    long_description=open('README.txt').read(),
    install_requires=[req.strip() for req in open('requirements.txt').readlines()],
)
