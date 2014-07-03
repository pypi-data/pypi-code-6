from setuptools import setup

setup(
    name='3lwg',
    description='Three Letter Word Game',
    py_modules=['tlw'],
    entry_points={
        'console_scripts': ['tlw = tlw:main']
    }
)
