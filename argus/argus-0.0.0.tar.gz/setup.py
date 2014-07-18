
from distutils.core import setup

setup(
    name='argus',
    version='0.0.0',
    author='Brandon Jackson and Dennis Evangelista',
    author_email='devangel77b@gmail.com',
    packages=['argus'],
    scripts=['bin/argus_audio_sync','bin/argus_initial_calibrate',
             'bin/argus_refine','bin/argus_detect_patterns',
             'bin/argus_undistort','bin/argus_simplified'],
    description='Helper routines for using multiple, inexpensive calibrated and synchronized cameras for 3D scientific use.',
    long_description=file('README.rst','r').read(),
    requires=[
        "opencv",
        "numpy",
        "pandas"
        ],
)
