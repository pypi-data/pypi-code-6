from setuptools import setup, find_packages

def read(filename):
    with open(filename) as fp:
        return fp.read()

setup(
    name='dockman',
    version='0.2',
    author='Mark McGuire',
    author_email='mark.b.mcg@gmail.com',
    url='http://github.com/TronPaul/dockman',
    description='A webservice that runs docker builds/deployments on docker webhooks',
    long_description=read('README.rst'),
    py_modules=['dockman'],
    zip_safe=False,
    install_requires=['flask', 'docker-py']
)
