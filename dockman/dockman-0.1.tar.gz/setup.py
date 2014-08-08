from setuptools import setup, find_packages

def read(filename):
    with open(filename) as fp:
        return fp.read()

setup(
    name='dockman',
    version='0.1',
    description='A webservice that runs docker builds/deployments on docker webhooks',
    long_description=read('README.rst'),
    author='Mark McGuire',
    author_email='mark.b.mcg@gmail.com',
    url='http://github.com/tronpaul/dockman',
    license='MIT',
    py_modules=['dockman'],
    install_requires=['flask', 'docker-py'],
    entry_points='''
    [console_scripts]
    dockman = dockman:run
    '''
)
