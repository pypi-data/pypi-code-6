from distutils.core import setup

setup(
    name='PGeoREST',
    version='0.1.1',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=['pgeorest'],
    url='http://pypi.python.org/pypi/PGeoREST/',
    license='LICENSE.txt',
    description='PGeoREST module.',
    long_description=open('README.txt').read(),
    install_requires=[
        'flask >= 0.10.1',
        'flask-cors >= 1.3.1',
        'pgeo >= 0.1.1'
    ]
)
