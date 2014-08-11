import os.path
import sys
from autotweet_web import __version__ as version

try:
    from setuptools import find_packages, setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import find_packages, setup


def readme():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
            return f.read()
    except (IOError, OSError):
        return ''


install_reqs = [
    'autotweet>=0.1.0',
    'flask>=0.10.1',
]
if sys.version_info < (3, 2):
    install_reqs.append('futures')


setup(
    name='autotweet-web',
    version=version,
    description='web instance for autotweet',
    long_description=readme(),
    url='http://kjwon15.net/',
    download_url='https://github.com/Kjwon15/autotweet-web/releases',
    author='Kjwon15',
    author_email='kjwonmail' '@' 'gmail.com',
    packages=find_packages(exclude=['tests']),
    install_requires=install_reqs,
)
