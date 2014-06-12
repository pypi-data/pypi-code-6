from distutils.core import setup

setup(
    name='django-glinks',
    version='0.1.3',
    author='Shawn Simon',
    author_email='shawn.simon.developer@gmail.com',
    packages=['glinks'],
    url='http://pypi.python.org/pypi/django-glinks/',
    license='LICENSE.txt',
    description='Interal add manager for django sites.',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.6.0",
    ],
)