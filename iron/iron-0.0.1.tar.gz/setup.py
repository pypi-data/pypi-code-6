"""
iron: the powerful but simple build tool using flows.
"""
from setuptools import setup, find_packages


setup(
    name='iron',
    version='0.0.1',
    url='https://github.com/nvie/iron',
    license='BSD',
    author='Vincent Driessen',
    author_email='vincent@3rdcloud.com',
    description=__doc__.strip(),
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['click', 'more_itertools'],
    entry_points={
        'console_scripts': [
            'iron = iron.cli:cli',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
