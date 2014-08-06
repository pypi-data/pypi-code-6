import os
from setuptools import setup

# %(name)s
# %(desc)s

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "%(name)s",
    version = "0.0.1",
    description = "%(desc)s",
    author = "%(author)s",
    author_email = "%(email)s",
    license = "GPLv3+",
    keywords = "%(keywords)s",
    url = "%(url)s",
    packages=['%(name)s'],
    package_dir={'%(name)s': '%(name)s'},
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
    entry_points = {
        'console_scripts': [
            '%(name)s = %(name)s.bin:%(name)s',
        ],
    },
    #package_data = {
        #'%(name)s': ['catalog/*.edb'],
    #},
    #include_package_data = True,
)
