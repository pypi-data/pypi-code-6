from setuptools import setup, find_packages

setup(
    name='getout',
    version='0.1.0.dev1',
    author='Bin Wang', 
    author_email='binwang.cu@gmail.com',
    license='MIT',
    install_requires=['beautifulsoup4'],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    entry_points={
        'console_scripts':['getout=getout.command_line:main'],
    },
)
