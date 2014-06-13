try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='melody-dl',
    packages=['melody_dl'],
    version='0.1.5',
    description='Command line utility that downloads audio files from various websites.',
    author='Simon W. Jackson | miniArray',
    author_email='simon@miniarray.com',
    url='http://melody-dl.com',
    download_url = 'https://github.com/miniarray/melody-dl/tarball/v0.1.5',
    keywords = ['download', 'music', 'audio'],
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    install_requires=[
        "mutagen == 1.23",
        "beautifulsoup4 == 4.3.2",
        "requests == 2.3.0",
        "docopt == 0.6.1",
        "progress2==1.1.0",
        "slimit==0.8.1",
    ],
)
