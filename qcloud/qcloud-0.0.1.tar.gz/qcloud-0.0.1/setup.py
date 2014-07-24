from setuptools import setup

#http://docs.python.org/2/distutils/setupscript.html

setup(
    name='qcloud',
    version='0.0.1',

    author='dev',
    author_email='dev@agutong.com',
    url='http://git.agutong.com/dev/qcloud',

    license='LICENSE',
    description='qcloud',
    long_description=open('README.md').read(),

    packages=[
      'qcloud',
    ],

    package_data = {
        #'qcloud': ['config/*.yml'],
    },

    data_files=[
        #('/etc/init.d', ['bin/init-qcloud'])
    ],

    scripts=[
        #'bin/qcloud'
    ],

    install_requires=[
        #"Django >= 1.1.1",
    ],

    dependency_links=[
        #zip/tar urls
    ]
)