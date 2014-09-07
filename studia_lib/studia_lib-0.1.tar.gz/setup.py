from setuptools import setup, find_packages

setup(
    name = "studia_lib",
    version = "0.1",
    packages = find_packages(),
    author = 'Wojciech Lichota',
    
    entry_points={
        'console_scripts': [
          'rmpyc = studia_lib.utils:remove_pyc',
        ],
    }
)