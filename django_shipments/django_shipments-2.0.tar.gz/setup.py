# coding: utf-8 -*-
from setuptools import setup


setup(
    name='django_shipments',
    version='2.0',
    description="Shipping interface for multiple carriers",
    keywords=['shipping', 'ship', 'ups'],
    author='Brian Lee',
    author_email='blee93@live.com',
    url='http://github.com/therealblee/django-ship',
    license='OSI',
    packages=['django_shipments'],
    package_data={'django_shipments': ['wsdl/*']},
    install_requires=['suds>=0.4'],
    test_suite="nose.collector"
)
