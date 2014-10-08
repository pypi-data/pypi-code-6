from distutils.core import setup

import MARDS

setup(
    name='MARDS',
    version=MARDS.__version__,
    author='Maker Redux Corporation',
    author_email='johnd@makerredux.com',
    packages=['MARDS'],
    url='https://github.com/MakerReduxCorp/MARDS',
    license='MIT',
    description='Support Library for MARDS data serialization',
    install_requires=[
        "rolne"
    ],
)