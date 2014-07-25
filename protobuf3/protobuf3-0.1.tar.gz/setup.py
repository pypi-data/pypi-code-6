from setuptools import setup

setup(
    name='protobuf3',
    version='0.1',
    packages=['protobuf3', 'protobuf3.compiler', 'protobuf3.fields'],
    scripts=['bin/protoc-gen-python3'],
    url='https://github.com/Pr0Ger/protobuf3',
    license='MIT',
    author='Pr0Ger',
    author_email='me@pr0ger.org',
    description='Protocol buffers library for Python 3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4'
    ]
)
