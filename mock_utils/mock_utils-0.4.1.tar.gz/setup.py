from setuptools import setup, find_packages

VERSION = '0.4.1'

setup(
    name='mock_utils',
    version=VERSION,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    url='https://gitlab.com/tarcisioe/mock_utils',
    download_url='https://gitlab.com/tarcisioe/mock_utils/repository/archive.tar.gz?ref=' + VERSION,
    keywords=['testing', 'mock', 'file'],
    maintainer='Tarcísio Eduardo Moreira Crocomo',
    maintainer_email='tarcisio.crocomo+pypi@gmail.com',
    description='Python package providing utilities for mocking stuff on Python.',
)
