from setuptools import setup, find_packages


__version__ = '0.0.2'


setup(
    name='twitter_apponly_auth',
    version=__version__,
    description="An API Client for Twitter's Application Only Authentication",
    author="Joel Taddei / @taddeimania",
    author_email="jtaddei@gmail.com",
    packages=['twitter_apponly_auth'],
    install_requires=['requests']
)
