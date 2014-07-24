from setuptools import setup

#http://docs.python.org/2/distutils/setupscript.html

setup(
    name='kuankr',
    version='0.0.1',

    author='dev',
    author_email='dev@agutong.com',
    url='http://git.agutong.com/dev/kuankr',

    license='LICENSE',
    description='kuankr',
    long_description=open('README.md').read(),

    packages=[
      'kuankr',
    ],

    package_data = {
        #'kuankr': ['config/*.yml'],
    },

    data_files=[
        #('/etc/init.d', ['bin/init-kuankr'])
    ],

    scripts=[
        #'bin/kuankr'
    ],

    install_requires=[
        #"Django >= 1.1.1",
    ],

    dependency_links=[
        #zip/tar urls
    ]
)