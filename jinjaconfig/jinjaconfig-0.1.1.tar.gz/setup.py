from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.pip')

setup(
    name='jinjaconfig',
    version='0.1.1',
    description='A jinja2 renderer receiving a JSON string from commandline. Useful for generating config \
    files in deployment enviroments',
    long_description="%s\n\n%s" % (open('README.rst', 'r').read(), open('AUTHORS.rst', 'r').read()),
    author='Luis Fernando Barrera',
    author_email='luisfernando@informind.com',
    license='MIT',
    url='https://bitbucket.org/luisfernando/jinjaconfig',
    packages=find_packages(),
    dependency_links=[],
    install_requires=[str(ir.req) for ir in install_reqs],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'jinjaconfig = jinjaconfig:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
