from setuptools import setup


packages = [
    'otlichno'
]


install_requires = [
    'django'
]

setup(
    name='otlichno',
    version='0.0.1',
    description='otlichno package',
    long_description='from otlichno import django',
    keywords='otlichno',
    author='hellraiser',
    author_email='hellraiser@ukr.net',
    url='https://www.google.com.ua/?q=django',
    license='BSD',
    packages=packages,
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
