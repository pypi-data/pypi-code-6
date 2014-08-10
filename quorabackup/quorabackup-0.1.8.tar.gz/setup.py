from distutils.core import setup

setup(
    name='quorabackup',
    version='0.1.8',
    author='Christopher J. Su',
    author_email='christophersu9@gmail.com',
    packages=['quorabackup'],
    url='http://pypi.python.org/pypi/quorabackup/',
    license='LICENSE.txt',
    description='A module to back up data from Quora.',
    long_description=open('README.txt').read(),
    install_requires=[
        "beautifulsoup4 == 4.3.2",
        "click == 2.4",
        "feedparser == 5.1.3",
        "pymongo == 2.7.2",
        "quora == 0.1.6",
        "requests == 2.3.0",
        "wsgiref == 0.1.2"
    ],
)