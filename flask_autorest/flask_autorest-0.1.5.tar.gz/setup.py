from setuptools import setup, find_packages

setup(
    name="flask_autorest",
    version='0.1.5',
    zip_safe=False,
    platforms='any',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=['flask', 'dataset'],
    url="https://github.com/dantezhu/flask_autorest",
    license="MIT",
    author="dantezhu",
    author_email="zny2008@gmail.com",
    description="auto create restful apis for database, with the help of dataset.",
)
