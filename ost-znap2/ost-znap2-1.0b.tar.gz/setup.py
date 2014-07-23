"""
Setup ost.znap2 library and znap2 command line script.
"""

from setuptools import setup


setup(
    name='ost-znap2',
    version='1.0b',
    description='ZoDB snapshotter library and script',
    url='https://bitbucket.org/kvas/ost-znap2',
    author='Vasily Kuznetsov',
    author_email='kvas.it@gmail.com',
    license='MIT',
    namespace_packages=['ost'],
    packages=['ost', 'ost.znap2'],
    install_requires=['click'],
    entry_points={
        'console_scripts': ['znap2 = ost.znap2.script:main']
    },
    zip_safe=True,
    classifiers=(
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
    )
)
