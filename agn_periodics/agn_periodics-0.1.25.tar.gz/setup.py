from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']


setup(
    name='agn_periodics',
    version='0.1.25',
    packages=['agn_periodics'],
    package_data={'agn_periodics': ['agn_periodics/*.json']},
    data_files=[('', ['agn_periodics/config.json'])],
    url='',
    license='GPL',
    author='yarnaid',
    author_email='yarnaid@gmail.com',
    description='Some statistical functions for searchin periodics in time rows'
)
