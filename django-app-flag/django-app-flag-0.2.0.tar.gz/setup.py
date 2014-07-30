from distutils.core import setup

setup(name = 'django-app-flag',
      version = '0.2.0',
      author = 'Joe Groseclose',
      author_email = 'joe.groseclose@example.com',
      packages = ['django_app_flag',
                  'django_app_flag.templates'
                  ],
      url='http://pypi.python.org/pypi/django_app_flag/',
      license='LICENSE.txt',
      description='Simple flag for your Django webapps',
      long_description=open('README.txt').read(),
      install_requires=["Django >= 1.6.5"],
      )
