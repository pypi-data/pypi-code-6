from distutils.core import setup

setup(
    name='django-coretext',
    version='0.5.0',
    author='Geert Dekkers',
    author_email='geert@djangowebstudio.nl',
    packages=['text',],
    scripts=[],
    url='http://pypi.python.org/pypi/django-coretext/',
    license='LICENSE.txt',
    description='DOM-based text editor',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.1.1",
    ],
)