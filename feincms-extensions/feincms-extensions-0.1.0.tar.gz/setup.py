from setuptools import setup, find_packages


version = '0.1.0'


install_requires = (
    'FeinCMS>=1.9,<1.10',
)

setup(
    name='feincms-extensions',
    packages=find_packages(),
    include_package_data=True,
    version=version,
    description='',
    long_description='',
    author='Incuna',
    author_email='admin@incuna.com',
    url='https://github.com/incuna/feincms-extensions/',
    install_requires=install_requires,
    zip_safe=False,
)
