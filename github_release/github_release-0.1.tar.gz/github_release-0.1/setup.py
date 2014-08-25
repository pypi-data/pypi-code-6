from setuptools import setup, find_packages
setup(name='github_release',
    version='0.1',
    description='Release to GitHub',
    author='Tom Petr',
    author_email='tpetr@hubspot.com',
    url='http://dev.hubspot.com/',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'github3.py==0.9.1',
    ],
    entry_points={
        'console_scripts': [
            'github_release = github_release:run',
        ],
    },
    platforms=['all'],
)