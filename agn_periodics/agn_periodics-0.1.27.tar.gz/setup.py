from distutils.core import setup

setup(
    name='agn_periodics',
    version='0.1.27',
    packages=['agn_periodics'],
    package_data={'agn_periodics': ['config.json']},
    data_files=[('agn_periodics', ['agn_periodics/config.json'])],
    url='',
    license='GPL',
    author='yarnaid',
    author_email='yarnaid@gmail.com',
    description='Some statistical functions for searchin periodics in time rows'
)
