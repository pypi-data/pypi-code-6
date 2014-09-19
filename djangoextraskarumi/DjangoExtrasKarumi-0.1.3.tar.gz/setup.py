from distutils.core import setup

setup(
    name='DjangoExtrasKarumi',
    version='0.1.3',
    author='Davide Mendolia',
    author_email='davide@karumi.com',
    packages=['django_extras_karumi', 'django_extras_karumi.test'],
    url='https://pypi.python.org/pypi/DjangoExtrasKarumi/',
    license='LICENSE',
    description='Extras classes for django projects.',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.6.0",
        "django-pipeline >= 1.3.21",
        "django-storages >= 1.1.8",
        "boto >= 2.32.1"
    ],
)