import os
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-simple-activity',
    version='0.1.1',
    packages=find_packages('src', exclude=('tests',)),
    package_dir={'': 'src'},
    include_package_data=True,
    license='Apache 2.0',
    description=(
        'Simple, generic, activity streams '
        'from the actions on your site.'),
    url='https://github.com/richardasaurus/django-simple-activity',
    author='Richard O\'Dwyer',
    author_email='richard@richard.do',
    zip_safe=True,
    install_requires=[
        'django>=1.5.0, <1.6.0',
        'django-model-utils>=2.2',
    ]
)
