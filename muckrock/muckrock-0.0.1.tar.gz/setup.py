from setuptools import setup, find_packages

setup(
    name='muckrock',
    version='0.0.1',
    description="Get data from Muckrock",
    author='Thomas Levine',
    author_email='_@thomaslevine.com',
    url='http://github.com/tlevine/muckrock',
    license='AGPL',
    py_modules=['muckrock'],
    install_requires=[
        'requests>=2.3.0',
        'picklecache>=0.0.4',
        'lxml>=3.3.5',
    ],
    tests_require=['nose'],
    scripts = 'muckrock',
)
