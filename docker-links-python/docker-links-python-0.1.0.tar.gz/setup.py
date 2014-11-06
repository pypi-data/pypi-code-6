import os

from setuptools import setup

setup(
    name='docker-links-python',
    version='0.1.0',
    description='A helper for parsing Docker link environment variables.',
    long_description=open('README.md').read() + '\n\n',
    url='https://github.com/JoakimSoderberg/docker-links-python',
    license='MIT',
    author='Joakim Soderberg',
    author_email='joakim.soderberg@gmail.com',
    py_modules=['docker_links'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

