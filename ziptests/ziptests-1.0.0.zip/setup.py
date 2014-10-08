__author__ = ['katelyn']

from setuptools import setup,find_packages

setup(
      name='ziptests',
      version='1.0.0',
      url='http://www.osforce.com',
      license='MIT',
      author='liuhang',
      author_email='liuhang-2005@163.com',
      description=[
            "Programming Language :: Python",
    ],
      platforms='any',
      keywords='framework zip testing',
      packages=find_packages(exclude=['tests'])
)