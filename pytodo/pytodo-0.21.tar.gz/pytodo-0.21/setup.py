from setuptools import setup

setup(
    name='pytodo',
    version='0.21',
    py_modules=['pytodo'],
    description='Todo lists for your terminal',
    url='http://github.com/itsnauman/tod',
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
        t=tod:main
    ''',
)
