from distutils.core import setup

setup(
    name='DjangoExtrasKarumi',
    version='0.1.1',
    author='Davide Mendolia',
    author_email='davide@karumi.com',
    packages=['django-extras-karumi', 'django-extras-karumi.test'],
    url='https://pypi.python.org/pypi/DjangoExtrasKarumi/',
    license='LICENSE',
    description='Extras classes for django projects.',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.6.0",
        "django-pipeline >= 1.3.21",
        "django-storages >= 1.1.8"
    ],
)