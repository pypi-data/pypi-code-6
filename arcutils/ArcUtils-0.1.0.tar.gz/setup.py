from distutils.core import setup

setup(
    name='ArcUtils',
    version='0.1.0',
    author='PSU ARC Staff',
    author_email='consultants@pdx.edu',
    packages=['arc_utils'],
    url='',
    license='LICENSE.txt',
    description='ARC Projects utility package',
    long_description=open('README.txt').read(),
    install_requires=[
        'Django == 1.6.5',
    ],
)
