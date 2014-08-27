# Geraldo setup

# Downloads setuptools if not find it before try to import
try:
    from setuptools import setup, find_packages
except:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from setuptools import setup
from geraldo.version import get_version

setup(
    name = 'CubicReport',
    version = get_version(),
    description = 'CubicReport is a report engine based on Geraldo for Odoo, OpenERP, Python and Django applications',
    long_description = 'CubicReport is report engine based on Geraldo Reports, Geraldo is a Python and Django pluggable application that works with ReportLab to generate complex reports.',
    author = 'Cubic ERP',
    author_email = 'info@cubicerp.com',
    url = 'http://www.cubicerp.com/',
    #download_url = 'http://ufpr.dl.sourceforge.net/sourceforge/geraldo/Geraldo-0.2-stable.tar.gz',
    license = 'GNU Lesser General Public License (LGPL)',
    packages = ['geraldo', 'geraldo.tests', 'geraldo.generators',],
    install_requires = ['reportlab',],
)
