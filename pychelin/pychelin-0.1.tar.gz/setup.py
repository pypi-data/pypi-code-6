from setuptools import setup, find_packages

version = '0.1'

setup(
    name='pychelin',
    version=0.1,
    description="Module that dialog with viamichelin api.",
    long_description="""This module will allow us to geocode addresses.
""",
    classifiers=[],
    keywords='pychelin',
    author='Anael Lorimier',
    author_email='anael.lorimier@xcg-consulting.fr',
    url='https://bitbucket.org/xcg/pychelin',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'requests',
        'iso3166',
    ],
    tests_require=[
    ],
)
