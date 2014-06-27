from setuptools import setup

setup(
    name='pytodo',
    version='0.20',
    py_modules=['pytodo'],
    description='pytodo is a simple command-line todo application',
    url='http://github.com/itsnauman/pytodo',
    author='Nauman Ahmad',
    author_email='nauman-ahmad@outlook.com',
    license='MIT',
    include_package_data=True,
    install_requires=[
        'termcolor',
        'docopt',
        'prettytable',
    ],
    entry_points='''
        [console_scripts]
        t=pytodo:main
    ''',
)
