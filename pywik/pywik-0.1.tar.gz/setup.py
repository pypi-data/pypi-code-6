from setuptools import setup

setup(name='pywik',
      version='0.1',
      description='Python API for Piwik HTTP interface',
      author='Jay Camp',
      author_email='jay.r.camp@gmail.com',
      url='http://github.com/jrcamp/pywik',
      packages=['pywik'],
      install_requires=['requests>=2.3.0'],
 )
