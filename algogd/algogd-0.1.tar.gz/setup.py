from setuptools import setup

setup(name='algogd',
      version='0.1',
      description='Algorithmic backtester for incorporating GDELT event data into finance analysis',
      url='http://github.com/nkarnik/algogd',
      author='Nikhil Karnik',
      author_email='n.karnik@yahoo.com',
      license='MIT',
      packages=['algogd'],
      install_requires=[
          'pandas',
          'sqlalchemy',
      ],
      zip_safe=False)
