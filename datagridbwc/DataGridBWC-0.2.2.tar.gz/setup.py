import os
from setuptools import setup, find_packages
from setuptools.command.develop import develop as STDevelopCmd

cdir = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(cdir, 'readme.rst')).read()
CHANGELOG = open(os.path.join(cdir, 'changelog.rst')).read()


class DevelopCmd(STDevelopCmd):
    def run(self):
        # add in requirements for testing only when using the develop command
        self.distribution.install_requires.extend([
            'nose',
            'mock',
            'xlwt',
            'xlrd',
            'WebTest',
        ])
        STDevelopCmd.run(self)

from datagridbwc import VERSION

setup(
    name='DataGridBWC',
    version=VERSION,
    description="A BlazeWeb component for turning SQLAlchemy recordsets into HTML tables",
    long_description=README + '\n\n' + CHANGELOG,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
    ],
    author='Randy Syring',
    author_email='randy@thesyrings.us',
    url='http://bitbucket.org/blazelibs/datagridbwc/',
    license='BSD',
    packages=find_packages(exclude=['datagridbwc_*']),
    tests_require=['webtest'],
    include_package_data=True,
    zip_safe=False,
    cmdclass={'develop': DevelopCmd},
    install_requires=[
        'BlazeUtils >=0.3.8',
        'BlazeWeb ==dev, >0.4.4',
        'SQLAlchemyBWC>=0.1',
        "python-dateutil",
        'WebGrid>=0.1.6',
    ],
)
