from setuptools import setup, find_packages
from distutils.sysconfig import get_python_lib


setup(
    name='quintet',
    version='1.0.0b3',
    url='http://www.quintet.io/',
    author='A.J. May',
    author_email='aj7may@gmail.com',
    description='A Bootstrapped Markdown CMS powered by Django',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=1.7.0',
        'django-bootstrap-markdown>=1.8.0',
        'django-bootstrap-typeahead>=1.1.5',
        'django-password-strength>=1.1.1',
        'django-forms-bootstrap>=3.0.0',
        'Markdown>=2.5',
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
    ],
)
