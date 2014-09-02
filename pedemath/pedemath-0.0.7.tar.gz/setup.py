
import pedemath

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='pedemath',
    version=pedemath.__version__,
    description="Pedemath is a Python Vector and Math library",
    author="Eric Olson",
    author_email="me@olsoneric.com",
    maintainer="Eric Olson",
    maintainer_email="me@olsoneric.com",
    url="http://github.com/olsoneric/pedemath",
    packages=['pedemath'],
    package_data={'': ['LICENSE', 'NOTICE', 'README.md']},
    package_dir={'pedemath': 'pedemath'},
    include_package_data=True,
    license='Apache 2.0',
    keywords=["vector", "math", "matrix", "quaternion"],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    long_description=readme,
)
