from distutils.core import setup

setup(name='circular',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Visualize the latest circular from the Somerville Market Basket',
      url='http://small.dada.pink/speakeasy',
      packages=['circular'],
      install_requires = [
          'pyfiglet>=0.7.1',
          'colorama>=0.3.1',
      ],
      scripts = [
          'bin/circular',
      ],
      tests_require = ['nose'],
      version='0.1',
      license='AGPL',
      classifiers=[
          'Programming Language :: Python :: 3.4',
      ],
)
