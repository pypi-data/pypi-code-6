"""
DataGridBWC
======================

Questions & Comments
---------------------

Please visit: http://groups.google.com/group/blazelibs

Source Code
---------------

The code is available from the `bitbucket repo <http://bitbucket.org/rsyring/datagridbwc/>`_.

The `DataGridBWC tip <http://bitbucket.org/rsyring/datagridbwc/get/tip.zip#egg=datagridbwc-dev>`_
is installable via `easy_install` with ``easy_install DataGridBWC==dev``
"""

from setuptools import setup, find_packages
from setuptools.command.develop import develop as STDevelopCmd

class DevelopCmd(STDevelopCmd):
    def run(self):
        # add in requirements for testing only when using the develop command
        self.distribution.install_requires.extend([
            'nose',
        ])
        STDevelopCmd.run(self)

from datagridbwc import VERSION

setup(
    name='DataGridBWC',
    version=VERSION,
    description="A BlazeWeb component for turning SQLAlchemy recordsets into HTML tables",
    long_description = __doc__,
    classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    ],
    author='Randy Syring',
    author_email='rsyring@gmail.com',
    url='http://bitbucket.org/rsyring/datagridbwc/',
    license='BSD',
    packages=find_packages(exclude=['datagridbwc_*']),
    tests_require=['webtest'],
    include_package_data=True,
    zip_safe=False,
    cmdclass = {'develop': DevelopCmd},
    install_requires=[
        'BlazeUtils >=0.3.8',
        'BlazeWeb ==dev, >0.4.4',
        'SQLAlchemyBWC>=0.1',
        "python-dateutil"
    ],
)
