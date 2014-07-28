from distutils.core import setup

setup(
    name='StandardDecimalNotation',
    version='0.0.0',
    author='Shawn David Pringle B.Sc.',
    author_email='sdavidpringle@hotmail.com',
    packages=['standarddecimalnotation', 'standarddecimalnotation.test'],
    scripts=[],
    url='https://pypi.python.org/pypi/StandardDecimalNotation',
    license='LICENSE.txt',
    description='Numbers in the UI exactly like you learned in school.',
    long_description=open('README.txt').read(),
)
