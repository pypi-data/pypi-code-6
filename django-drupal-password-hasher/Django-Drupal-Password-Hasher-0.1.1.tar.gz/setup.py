try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='Django-Drupal-Password-Hasher',
    version='0.1.1',
    author='ARC Staff, pberndt',
    author_email='consultants@pdx.edu',
    packages=['djangodrupalpasswordhasher','djangodrupalpasswordhasher.test'],
    url='http://pypi.python.org/pypi/Django-drupal-password-hasher/',
    license='LICENSE.txt',
    description='Useful password hasher for django sites with drupal components',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.6.5",    
    ],
)
