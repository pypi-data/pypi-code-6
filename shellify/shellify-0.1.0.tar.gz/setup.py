import os
from setuptools import setup

# shellify
# Turn any python module into a shell!

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "shellify",
    version = "0.1.0",
    description = "Turn any python module into a shell!",
    author = "Johan Nestaas",
    author_email = "johannestaas@gmail.com",
    license = "GPLv3+",
    keywords = "shell python command line cli terminal",
    url = "https://bitbucket.org/johannestaas/shellify",
    packages=['shellify'],
    package_dir={'shellify': 'shellify'},
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
    ],
    #entry_points = {
        #'console_scripts': [
        #    'shellify = shellify.bin:shellify',
        #],
    #},
    #package_data = {
        #'shellify': ['catalog/*.edb'],
    #},
    #include_package_data = True,
)
