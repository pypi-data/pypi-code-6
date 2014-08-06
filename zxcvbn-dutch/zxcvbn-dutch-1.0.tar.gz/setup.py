from distutils.core import setup

setup(name='zxcvbn-dutch',
      version='1.0',
      description='Password strength estimator with Dutch support',
      author='Erik Romijn',
      author_email='github@erik.io',
      url='https://www.github.com/erikr/python-zxcvbn',
      packages=['zxcvbn'],
      package_data={'zxcvbn': ['generated/frequency_lists.json', 'generated/adjacency_graphs.json']}
     )
