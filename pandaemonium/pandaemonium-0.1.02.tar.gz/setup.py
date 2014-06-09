from distutils.core import setup
from glob import glob
import os

long_desc = open('pandaemonium.README').read()

setup( name='pandaemonium',
       version= '0.1.02',
       license='BSD License',
       description='Framework for writing daemons, with API similar to threading and multiprocessing.',
       long_description=long_desc,
       py_modules=['pandaemonium'],
       provides=['pandaemonium'],
       author='Ethan Furman',
       author_email='ethan@stoneleaf.us',
       classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            'Topic :: Software Development',
            ],
    )

