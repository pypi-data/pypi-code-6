try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='arrow-fatisar',
    version='0.4.4',
    description='("arrow" fork) Better dates and times for Python, with intervals',
    url='https://github.com/fatisar/arrow',
    author='Daniel Sarfati',
    author_email="fatisar@gmail.com",
    license='Apache 2.0',
    packages=['arrow'],
    zip_safe=False,
    install_requires=[
        'python-dateutil'
    ],
    test_suite="tests",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

