from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='bosrvclient',
    version='0.1',
    packages=find_packages(),

    install_requires=[
        'thrift'
    ],

    author='MacroData Inc',
    author_email='info@macrodatalab.com',
    description='BigObject service client for python',
    long_description=readme(),
    license='Apache 2.0',
    keywords=[
        'bigobject',
        'macrodata',
        'analytics'
    ],
    url='https://bitbucket.org/macrodata/bosrvclient-py.git',

    zip_safe=False
)
