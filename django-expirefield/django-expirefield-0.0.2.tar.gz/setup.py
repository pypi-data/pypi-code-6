from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-expirefield',
    version='0.0.2',
    author='Jarrell Waggoner',
    author_email='malloc47@gmail.com',
    download_url='https://github.com/malloc47/expirefield/tarball/master#egg=expirefield-0.0.2',
    dependency_links = ['https://github.com/malloc47/expirefield/tarball/master#egg=expirefield-0.0.2'],
    packages=find_packages(),
    url='https://github.com/malloc47/django-expirefield',
    license='LICENSE.txt',
    description='ExpireField for django models that will remove fields at regular intervals',
    install_requires=[
        "Django",
    ],
)

