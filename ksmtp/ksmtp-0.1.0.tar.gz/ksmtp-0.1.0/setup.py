from distutils.core import setup

setup(
    name='ksmtp',
    version='0.1.0',
    author='Kenneth Burgener',
    author_email='kenneth@k.ttak.org',
    scripts=['bin/ksmtp'],
    packages=['ksmtp'],
    package_data={'ksmtp': ['conf/*.conf']},
    url='http://pypi.python.org/pypi/ksmtp/',
    license='LICENSE.txt',
    description='Simple Python SMTP relay replacement for sendmail with SSL authentication',
    long_description=open('README.md').read(),
)
