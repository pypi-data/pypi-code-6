from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='json_manipulate',
    version='0.1',
    description='Manipulate JSON strings from the command line.',
    url='http://github.com/dporru/json_manipulate',
    author='Daan Porru',
    author_email='daanporru@gmail.com',
    license='GPLv3',
    packages=['json_manipulate'],
    zip_safe=False,
    entry_points = {
        'console_scripts': ['json_manipulate=json_manipulate.json_manipulate:main']
    },
    test_suite='nose.collector',
    tests_require=['nose']
)

