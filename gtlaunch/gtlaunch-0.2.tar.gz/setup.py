import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='gtlaunch',
    version=__import__('gtlaunch').__version__,
    description='Gnome Terminal launcher',
    long_description=read('README.rst'),
    author='Zbigniew Siciarz',
    author_email='zbigniew@siciarz.net',
    url='http://github.com/zsiciarz/gtlaunch',
    download_url='http://pypi.python.org/pypi/gtlaunch',
    license='MIT',
    packages=find_packages(),
    platforms='any',
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'gtlaunch = gtlaunch.main:run',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities'
    ],
)
