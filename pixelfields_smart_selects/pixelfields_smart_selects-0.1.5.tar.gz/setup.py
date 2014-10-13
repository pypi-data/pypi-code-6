import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='pixelfields_smart_selects',
    version='0.1.5',
    packages=['pixelfields_smart_selects'],
    include_package_data=True,
    description='Smart selects for Django >= 1.7',
    long_description=README,
    url='https://bitbucket.org/pixelfields/smart-selects',
    download_url='https://bitbucket.org/pixelfields/smart-selects/get/v0.1.5.tar.gz',
    author='pixelfields',
    author_email='pixelfields@runbox.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ],
    keywords=['django', 'admin', 'chained', 'selects'],
    install_requires=[
        "Django>=1.7",
	"simplejson",
    ],
)
