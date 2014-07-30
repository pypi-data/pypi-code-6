from distutils.core import setup

setup(name = 'django-simple-error',
      version = '0.3.0',
      author = 'Joe Groseclose',
      author_email = 'joe.groseclose@example.com',
      packages = ['django_simple_error'],
      url='http://pypi.python.org/pypi/testpackage/',
      license='LICENSE.txt',
      description='Simple error page management',
      long_description=open('README.txt').read(),
      install_requires=["Django >= 1.6.5"],
      )
