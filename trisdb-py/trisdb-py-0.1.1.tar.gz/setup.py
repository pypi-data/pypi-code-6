from distutils.core import setup

setup(
    name = 'trisdb-py',
    py_modules = ['trisdb', 'message_pb2'],
    version = '0.1.1',
    description = 'The Python interface to TrisDb',
    author = 'Gianluca Tiepolo',
    author_email = 'tiepolo.gian@gmail.com',
    long_description=open('README.md').read(),
    url = 'https://github.com/tiepologian/trisdb-py',
    keywords = ['trisdb', 'python'],
    classifiers = [],
    install_requires=[
"protobuf",
    ],
)
