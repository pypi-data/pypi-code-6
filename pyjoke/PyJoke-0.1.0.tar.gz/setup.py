from distutils.core import setup

setup(
    name='PyJoke',
    version='0.1.0',
    author='Laurent Fite',
    author_email='laurent.fite@gmail.com',
    packages=['pyjoke'],
    scripts=['bin/str2joke.py'],
    url='http://pypi.python.org/pypi/PyJoke/',
    license='LICENSE.txt',
    description='Fetch the best joke in database.',
    long_description=open('README.txt').read(),
    install_requires=[
        "MySQLdb",
        "SQLite",
        "NLTK",
    ],
)
