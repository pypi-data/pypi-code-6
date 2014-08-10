from distutils.core import setup

setup(
    name='DjangoRequestLogger',
    version='0.2.0',
    author='Evgeny Morozov',
    author_email='python-code@realityexists.net',
    packages=['django_request_logger', 'django_request_logger.test'],
    url='http://pypi.python.org/pypi/DjangoRequestLogger/',
    license='LICENSE.txt',
    description='Django app to add current username, client IP, etc. to logging output.',
    long_description='''
This Django app adds extra fields to log records emitted
by the standard Python logging. Currently these include:

* username - Username of the currently logged in Django user, if any. If no
  user is logged in the value is "_" (distinct from empty string, which means
  that the information is not available).
* client_ip - IP address of the client browser, obtained from REMOTE_ADDR and
  HTTP_X_FORWARDED_FOR.
* absolute_url - the absolute URL of the current request, including the query
  string.
* raw_post_data - the raw POST data for the current request, if any.

These fields are then available to be used in your logging formatter (see
example below). They are also visible in Django Sentry as additional data (if
you have Django Sentry installed).
'''
)
