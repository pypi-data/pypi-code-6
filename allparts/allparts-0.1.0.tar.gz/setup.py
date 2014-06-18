"""amsin is a simple command line tool to shortlink an
amazon URL.

"""
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='allparts',
    description="A tool to merge all part files in an s3 bucket.",
    version='0.1.0',
    long_description=__doc__,
    packages=['allparts'],
    author='Anthony Grimes',
    author_email='i@raynes.me',
    url='https://github.com/Raynes/allparts',
    license='MIT',
    install_requires=requirements,
    entry_points = """
    [console_scripts]
    allparts=allparts.__main__:allparts
    """
)
