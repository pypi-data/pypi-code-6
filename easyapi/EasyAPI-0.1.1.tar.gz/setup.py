from distutils.core import setup

setup(
    name='EasyAPI',
    version='0.1.1',
    author='Adrian Czebiniak',
    author_email='adrian@artivest.co',
    packages=['easy_api', 'easy_api.test'],
    url='http://pypi.python.org/pypi/EasyAPI/',
    license='LICENSE.txt',
    description='A generic RESTful API interface for Python',
    long_description=open('README.rst').read(),
    install_requires=[
    ],
)
