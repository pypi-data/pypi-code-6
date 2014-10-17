from setuptools import setup, find_packages


version = '1.0.0'


setup(
    name='django-field-cryptography',
    packages=find_packages(),
    include_package_data=True,
    version=version,
    license='BSD',
    description='An encrypted field for Django.',
    install_requires=('cryptography>=0.6,<0.7',),
    author='Incuna Ltd',
    author_email='admin@incuna.com',
    url='https://github.com/incuna/django-field-cryptography',
)
