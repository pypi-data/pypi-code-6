from setuptools import setup

setup(
    name='3lwg',
    version='4.0',
    description='Three Letter Word Game',
    packages=['tlw'],
    package_data={
	'tlw': ['words.txt']
    },
    entry_points={
        'console_scripts': ['tlw = tlw:main']
    }
)
