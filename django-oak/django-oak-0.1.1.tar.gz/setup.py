import os

try:
    from setuptools import setup
except (ImportError):
    from distribute import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'django-oak',
    version = '0.1.1',
    packages = ['oak'],
    include_package_data = True,
    license = 'BSD License',
    description = 'Rapid prototyping for views and models in django.',
    long_description = README,
    url = 'https://github.com/weholt/django-oak',
    author = 'Thomas A. Weholt',
    author_email = 'thomas@weholt.org',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    requires=['django'],
    )