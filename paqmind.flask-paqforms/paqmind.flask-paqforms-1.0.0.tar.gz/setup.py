from setuptools import setup, find_packages


setup(
    name = 'paqmind.flask-paqforms',
    version = '1.0.0',
    license = 'Creative Commons Attribution-Noncommercial-Share Alike license',
    requires = ['markupsafe', 'babel', 'jinja2'],
    packages = find_packages(),
    include_package_data = True,
)
