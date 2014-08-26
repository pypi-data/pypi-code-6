from setuptools import setup, find_packages

setup(
    name = 'Flask-Edits',
    version = '0.7',
    packages = find_packages(),
    install_requires = ['flask',],
    license = 'BSD',
    url = 'http://github.com/nathancahill/flask-edits',
    author = 'Nathan Cahill',
    author_email='nathan@nathancahill.com',
    description='Editable Content in Flask',
    long_description=open('README').read(),
    package_data={'': ['*.css', '*.js', '*.map', '*.j2', '*.eot', '*.svg', '*.ttf', '*.woff']},
)
