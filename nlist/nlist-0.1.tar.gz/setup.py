from setuptools import setup
from os import path


project_dir = path.abspath(path.dirname(__file__))

def read_from(filename):
    with open(path.join(project_dir, filename), encoding='utf-8') as f:
        return f.read().strip()


setup(
    name='nlist',
    version=read_from('VERSION'),
    description='A lightweight multidimensional list in Python',
    long_description=read_from('README.rst'),
    url='https://github.com/swarmer/nlist',
    author='Anton Barkovsky',
    author_email='anton@swarmer.me',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='array list container multidimensional',
    py_modules=['nlist'],
    install_requires=[],
    include_package_data=True,
)
