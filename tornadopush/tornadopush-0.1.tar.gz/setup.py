from setuptools import setup, find_packages


setup(
    name='tornadopush',
    version='0.1',
    url='http://github.com/frascoweb/tornadopush',
    license='MIT',
    author='Maxime Bouroumeau-Fuseau',
    author_email='maxime.bouroumeau@gmail.com',
    description='Push and presence server built with Tornado and Redis',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'tornado>=4.0.2',
        'redis>=2.10.3',
        'itsdangerous>=0.24',
        'PyYAML>=3.11',
        'jsmin>=2.0.11',
        'brukva==0.0.1'
    ],
    dependency_links=[
        'https://github.com/evilkost/brukva/tarball/master#egg=brukva-0.0.1'
    ],
    entry_points='''
        [console_scripts]
        tornadopush=tornadopush.cli:main
    '''
)