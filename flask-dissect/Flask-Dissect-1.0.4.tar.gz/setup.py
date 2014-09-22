from setuptools import setup

setup(
    name='Flask-Dissect',
    version='1.0.4',
    url='http://bit.epix.com.br/flask-dissect/',
    license='BSD',
    author='Leandro Martelli',
    author_email='martelli@epix.com.br',
    description='Dissect Distributed Session Control',
    long_description=__doc__,
    packages=['flask_dissect'],
    platforms='any',
    install_requires=[
        'Flask', 'requests', 'pycrypto'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
