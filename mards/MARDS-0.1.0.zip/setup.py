from distutils.core import setup

setup(
    name='MARDS',
    version='0.1.0',
    author='Maker Redux Corporation',
    author_email='johnd@makerredux.com',
    packages=['MARDS'],
    url='https://github.com/MakerReduxCorp/MARDS',
    license='MIT',
    description='Support Library for MARDS data serialization',
    long_description=open('README.md').read(),
    install_requires=[
        "rolne"
    ],
)