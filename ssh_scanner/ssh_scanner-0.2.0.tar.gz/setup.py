import os
from setuptools import setup

# ssh_scanner
# Scan for SSH and store in a db

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "ssh_scanner",
    version = "0.2.0",
    description = "Scan for SSH and store in a db",
    author = "Johan Nestaas",
    author_email = "johannestaas@gmail.com",
    license = "GPLv3+",
    keywords = "",
    url = "https://bitbucket.org/johannestaas/ssh_scanner",
    packages=['ssh_scanner'],
    package_dir={'ssh_scanner': 'ssh_scanner'},
    long_description=read('README.md'),
    classifiers=[
        #'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
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
        'sqlalchemy',
        'psycopg2', # requires libpq-dev
    ],
    entry_points = {
        'console_scripts': [
            'ssh_scanner = ssh_scanner.bin:ssh_scanner',
        ],
    },
    #package_data = {
        #'ssh_scanner': ['catalog/*.edb'],
    #},
    #include_package_data = True,
)
