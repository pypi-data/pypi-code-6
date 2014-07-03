import codecs
import os
from setuptools import setup, find_packages


HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(HERE, *parts), 'r').read()


setup(
    name='kafka-dev-tools',
    version='0.0.1',
    author='Neha Narkhede',
    author_email='neha.narkhede@gmail.com',
    maintainer='Evgeny Vereshchagin',
    maintainer_email='evvers@ya.ru',
    url='https://github.com/evvers/kafka-dev-tools',
    description='Tools for Kafka developers',
    long_description=read('README.rst'),
    packages=find_packages(),
    install_requires=[
        'jira-python',
        'RBTools',
    ],
    entry_points = {
        'console_scripts': [
            'kafka-patch-review=kafka_dev_tools.utils.kafka_patch_review:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='kafka',
)
