# -*- coding: utf-8 -*-
import os

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='il2fb-commons',
    version='0.9.2',
    description="Common helpers and data structures for projects related to "
                "IL-2 Forgotten Battles",
    long_description=README,
    keywords=[
        'il2', 'il-2', 'fb', 'forgotten battles', 'commons',
    ],
    license='LGPLv3',
    url='https://github.com/IL2HorusTeam/il2fb-commons',
    author='Alexander Oblovatniy',
    author_email='oblovatniy@gmail.com',
    packages=[
        'il2fb.commons',
    ],
    namespace_packages=[
        'il2fb',
    ],
    install_requires=[
        i.strip() for i in open("requirements.txt").readlines()
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries',
    ],
    platforms=[
        'any',
    ],
)
