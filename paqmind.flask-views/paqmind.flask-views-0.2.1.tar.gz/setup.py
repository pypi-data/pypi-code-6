from setuptools import setup, find_packages

setup(
    name = 'paqmind.flask-views',
    description = 'Class-based views for Flask',
    version = '0.2.1',
    license = 'MIT',
    install_requires = ['flask', 'paqmind.flask-routes>=0.2.1'],
    packages = find_packages(),
    include_package_data = True,
)
