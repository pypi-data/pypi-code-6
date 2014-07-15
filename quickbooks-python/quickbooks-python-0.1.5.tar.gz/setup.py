from setuptools import setup, find_packages

setup(
    name='quickbooks-python',
    url='https://github.com/naudo/quickbooks-python',
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
        'rauth'
    ]
)
