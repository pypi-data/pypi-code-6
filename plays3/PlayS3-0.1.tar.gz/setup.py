from setuptools import setup

setup(name='PlayS3',
      version='0.1',
      description='Python library for working directly on Amazon S3',
      url='',
      author='Naren Arya',
      author_email='narenarya@live.com',
      license='MIT',
      packages=['PlayS3'],
      install_requires=[
          'FileChunkIO',
      ],
      zip_safe=False)