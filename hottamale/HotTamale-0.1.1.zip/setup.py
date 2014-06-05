import sys
from esky import bdist_esky
from distutils.core import setup

if sys.platform in ['win32','win564','cygwin']:

    setup(
        name='HotTamale',
        version='0.1.1',
        author='Kyle Ondy',
        author_email='KyleOndy@gmail.com',
        packages=['hottamale'],
        url='http://pypi.python.org/pypi/HotTamale/',
        license='LICENSE.txt',
        description='Spiceworks ticket display and notifier.',
        long_description=open('README.txt').read(),
        install_requires=[
            "Flask >= 0.10.1",
        ],
        scripts=["HotTamale.py"],
        options={"bdist_esky": {
            "freezer_module":"py2exe",
        }}
    )