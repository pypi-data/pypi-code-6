from distutils.core import setup

setup(
    name='MARDS',
    version='0.1.14',
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