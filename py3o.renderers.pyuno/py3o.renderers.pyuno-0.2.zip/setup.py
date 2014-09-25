from setuptools import setup, find_packages

version = '0.2'

setup(
    name='py3o.renderers.pyuno',
    version=version,
    description="A pyuno based driver for py3o",
    long_description="{}{}".format(
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
    ),
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='OpenOffice PDF',
    author='Florent Aide',
    author_email='florent.aide@gmail.com',
    url='https://bitbucket.org/faide/py3o.renderers.pyuno',
    license='MIT License',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['py3o'],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'setuptools',
    ],
    entry_points=dict(
        # -*- Entry points: -*-
    ),
    test_suite='nose.collector',
)
