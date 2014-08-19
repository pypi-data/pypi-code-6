from distutils.core import setup

setup(name='scarsdale-trustees',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Download minutes and agendas for Scarsdale Board of Trustees meetings',
      url='https://github.com/tlevine/scarsdale-trustees',
      py_modules = ['scarsdale_trustees'],
      install_requires = [
          'picklecache>=0.0.5',
          'pickle-warehouse>=0.1.1',
          'requests>=2.3.0',
          'lxml>=3.3.5',
      ],
      scripts = [
          'scarsdale-trustees',
      ],
      tests_require = ['nose'],
      version='0.0.1',
      license='AGPL',
      classifiers=[
          'Programming Language :: Python :: 3.4',
      ],
)
