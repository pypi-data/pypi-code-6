from setuptools import setup

setup(name='net_health',
      version='0.1',
      description='check network connectivity',
      url='',
      author='Gilad Zohari',
      author_email='gzohari@gmail.com',
      scripts=['bin/check_connectivity'],
      license='MIT',
      install_requires=[
          'python-neutronclient', 'python-novaclient'
      ],
      packages=['net_health'],
      zip_safe=False)
