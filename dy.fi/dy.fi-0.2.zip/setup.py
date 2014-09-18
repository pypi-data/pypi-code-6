from setuptools import find_packages
from setuptools import setup


setup(
    name='dy.fi',
    version='0.2',
    description="Adds commands to check dynamic IP address change and inform currenty IP address to dy.fi.",
    long_description=open("README.rst").read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7"],
    keywords='',
    author='Taito Horiuchi',
    author_email='taito.horiuchi@gmail.com',
    url='https://github.com/taito/dy.fi',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['dy'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools', 'ipgetter'],
    entry_points="""
    [console_scripts]
    dyfi = dy.fi:update_ip
    dyfi-last-updated =dy.fi:last_updated
    """)
