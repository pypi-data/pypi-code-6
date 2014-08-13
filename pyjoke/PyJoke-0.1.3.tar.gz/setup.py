from distutils.core import setup

setup(
    name='PyJoke',
    version='0.1.3',
    author='Laurent Fite',
    author_email='laurent.fite@gmail.com',
    packages=['pyjoke'],
    scripts=[],
    url='http://pypi.python.org/pypi/PyJoke/',
    license='LICENSE.txt',
    description='PyJoke: Fetch your jokes in Python.',
    long_description=open('README.txt').read(),
    install_requires=[
        "nltk == 2.0.4",
        "PyYAML==3.11",
    ],
)
