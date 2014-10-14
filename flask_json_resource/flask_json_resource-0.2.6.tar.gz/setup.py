from setuptools import setup


__VERSION__ = '0.2.6'

setup(
    name='flask_json_resource',
    version=__VERSION__,
    packages=['flask_json_resource', 'flask_json_resource.features',
              'flask_json_resource.features.steps'],
    package_data={
        'flask_json_resource': ['features/steps/schemas/*.json']
    },
    long_description=open('./README.rst').read(),
    author='Ernst Odolphi',
    author_email='ernst.odolphi@gmail.com',
    install_requires=['flask', 'json_resource', 'flask-pymongo'],
    tests_require=['behave', 'ensure'],
)




