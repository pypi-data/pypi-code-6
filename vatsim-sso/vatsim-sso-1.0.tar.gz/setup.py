from setuptools import setup

setup(
    name='vatsim-sso',
    version='1.0',
    packages=['vatsim_sso'],
    install_requires=['requests_oauthlib', 'requests'],
    url='https://bitbucket.org/nharasym/vatsim-sso',
    license='MIT Licence',
    author='Nick Harasym',
    author_email='saitekx50@me.com',
    description='Easy to use wrapper for vatsim sso'
)
