from distutils.core import setup

requirements = [
    'OSExtension>=0.1.3',
    'PyGithub>=1.25.0',
    'PyYAML>=3.11',
    'sh>=1.09',
]

setup(
    name='sync-github-forks',
    version='0.1.1',
    author='Andrew Udvare',
    author_email='audvare@gmail.com',
    packages=['ugf'],
    url='http://pypi.python.org/pypi/sync-github-forks/',
    license='LICENSE.txt',
    description='Extension for os module, for POSIX systems only',
    long_description=open('README.txt').read(),
    scripts=['bin/sync-github-forks'],
    install_requires=requirements,
)
