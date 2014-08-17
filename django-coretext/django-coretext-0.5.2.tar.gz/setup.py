from setuptools import setup, find_packages

setup(
    name='django-coretext',
    version='0.5.2',
    author='Geert Dekkers',
    author_email='geert@djangowebstudio.nl',
    packages=find_packages(),
    include_package_data = True,
    package_data = {
        '': ['*.txt', '*.rst'],
        'text': ['*.html'],
    },
    scripts=[],
    url='http://pypi.python.org/pypi/django-coretext/',
    license='LICENSE.txt',
    description='DOM-based text editor',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.1.1",
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)