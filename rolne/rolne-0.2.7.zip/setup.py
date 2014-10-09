from distutils.core import setup

import rolne

setup(
    name='rolne',
    version=rolne.__version__,
    author='Maker Redux Corporation',
    author_email='johnd@makerredux.com',
    packages=['rolne'],
    url='https://github.com/MakerReduxCorp/rolne',
    license='MIT',
    description='rolne: recursive ordered lists of named elements',
)
