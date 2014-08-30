from setuptools import setup

setup(
    name='UwoCalendar',
    author='Peter Argall',
    author_email='peter@argall.ca',
    description='Python script that grabs your schedule from student.uwo.ca and creates a handy ics file',
    url='https://github.com/pargall/UWO-Cal',
    version='3.0.0',
    packages=['uwoCalendar',],
    license='LICENSE.txt',
    long_description=open('README.txt').read(),
    install_requires=[
        "icalendar >= 3.0",
        "lxml >= 3.3.5",
    ],
)
