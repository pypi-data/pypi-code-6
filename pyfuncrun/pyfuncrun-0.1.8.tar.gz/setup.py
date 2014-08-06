from setuptools import setup

setup(
    name='pyfuncrun',
    version='0.1.8',
    py_modules=['pyfuncrun'],
    entry_points={
        'console_scripts': [
            'pyfuncrun=pyfuncrun:main',
            ]
        },
    url='https://github.com/zhangliyong/pyfuncrun',
    license='BSD',
    author='Lyon Zhang',
    author_email='lyzhang87@gmail.com',
    description='A tool to run a python function in a module from command line',
    long_description=open('README.rst').read()
)
