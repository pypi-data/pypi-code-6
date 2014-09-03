from distutils.core import setup

setup(
    name='PGeo',
    version='0.1.4',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=['pgeo.config',
              'pgeo.dataproviders',
              'pgeo.db',
              'pgeo.error',
              'pgeo.geoserver',
              'pgeo.gis',
              'pgeo.manager',
              'pgeo.metadata',
              'pgeo.publish',
              'pgeo.stats',
              'pgeo.thread',
              'pgeo.utils'],
    url='http://pypi.python.org/pypi/PGeo/',
    license='LICENSE.txt',
    description='PGeo module.',
    long_description=open('README.md').read()
)
