from setuptools import setup, find_packages

#next time:
#python setup.py register
#python setup.py sdist upload

version = open('classymq/VERSION', 'r').readline().strip()

long_desc = """
Class based RabbitMQ library. 

[Documentation](https://classymq.readthedocs.org/en/latest/)

[Report a Bug](https://github.com/gdoermann/classymq/issues)

[Users Mailing List](https://groups.google.com/forum/?fromgroups#!forum/classymq)
"""

setup(
    name='classymq',
    version=version,
    description='RabbitMQ class based library.',
    long_description=long_desc,
    classifiers = [
        "Environment :: Web Environment",
        "Environment :: Plugins",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='rabbitmq,amqp,messaging',
    install_requires = ['pika >= 0.9.5', 'txamqp', 'twisted'],
    author='Greg Doermann',
    author_email='gdoermann@gmail.com',
    url='https://github.com/gdoermann/classymq',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
)

