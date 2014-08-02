import os
from setuptools import setup

# buff
# Buffer and protocol builder and designer

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "buff",
    version = "0.0.1",
    description = "Buffer and protocol builder and designer",
    author = "Johan Nestaas",
    author_email = "johannestaas@gmail.com",
    license = "GPLv3+",
    keywords = "",
    url = "https://bitbucket.org/johannestaas/buff",
    packages=['buff'],
    package_dir={'buff': 'buff'},
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        #'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=[
    ],
    entry_points = {
        'console_scripts': [
            'buff = buff.bin:buff',
        ],
    },
    #package_data = {
        #'buff': ['catalog/*.edb'],
    #},
    #include_package_data = True,
)
