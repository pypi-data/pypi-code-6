import os
from setuptools import setup

# ultratransmission
# Automatically trigger torrents to download through transmission web client

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "ultratransmission",
    version = "1.6.2",
    description = "Automatically trigger torrents to download through transmission web client",
    author = "Johan Nestaas",
    author_email = "johannestaas@gmail.com",
    license = "GPLv3+",
    keywords = "pirate bay transmission torrent magnet",
    url = "https://bitbucket.org/johannestaas/ultratransmission",
    packages=['ultratransmission'],
    package_dir={'ultratransmission': 'ultratransmission'},
    #long_description=read('README.md'),
    classifiers=[
        #'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        #'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
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
        'ThePirateBay',
        'requests',
    ],
    entry_points = {
        'console_scripts': [
            'ultratransmission = ultratransmission.bin:main',
        ],
    },
    #package_data = {
        #'ultratransmission': ['catalog/*.edb'],
    #},
    #include_package_data = True,
)
