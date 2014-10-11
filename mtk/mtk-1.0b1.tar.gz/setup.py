from setuptools import setup
from setuptools import find_packages

# Create a pypi account and have a $HOME/.pypirc with that info

# To register the project in pypi (just once):
# $ python setup.py register

# To create a source distribution and upload to pypi:
# $ python setup.py sdist upload

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='mtk',
      #version='1.0',
      version='1.0b1',
      description='The Messaging ToolKit',
      long_description=readme(),
      classifiers=[
        #'Development Status :: 5 - Production/Stable',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Topic :: Communications',
      ],
      keywords='messaging publish subscribe amqu',
      url='https://bitbucket.org/wwsmith/mtk',
      author='Warren Smith',
      author_email='wsmith@tacc.utexas.edu',
      license='Apache',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
