
from setuptools import setup

setup(name='TheZine',
      version='0.0.1',
	  install_requires=['BeautifulSoup4>=4.3.1', 'requests'],
      description='Python API for The Zine',
	  long_description='Unofficial Python API for the blog http://thezine.biz. Usage: https://github.com/karan/HackerNewsAPI.',
      url='http://github.com/voidabhi/TheZineAPI',
      author='Abhijeet Mohan',
      author_email='abhijeetshibu@gmail.com',
      license='MIT',
      packages=['tz','tests'],
      zip_safe=False)