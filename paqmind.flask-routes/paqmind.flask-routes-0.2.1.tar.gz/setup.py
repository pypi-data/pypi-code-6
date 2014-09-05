from setuptools import setup, find_packages

setup(
    name = 'paqmind.flask-routes',
    description = 'Class-based routes for Flask',
    version = '0.2.1',
    license = 'MIT',
    requires = ['flask'],
    packages = find_packages(),
    include_package_data = True,
)
