# http://www.28lines.com/?p=8
import os
import re
from setuptools import setup, find_packages
from setuptools.command.test import test

long_description = """
Core of the jumbo framework from Thunder Systems.
"""


class TestRunner(test):
    def run(self, *args, **kwargs):
        if self.distribution.install_requires:
            self.distribution.fetch_build_eggs(
                self.distribution.install_requires)
        if self.distribution.tests_require:
            self.distribution.fetch_build_eggs(
                self.distribution.tests_require)
        from jmb.core.tests.runtests import runtests
        runtests()


def get_data_files(*args, **kwargs):

    EXT_PATTERN = kwargs.get('ext') or '\.(html|js|txt|css|po|mo|jpg|png|gif|ico)'

    data_dict = {}
    for pkg_name in args:
        data_files = []
        for dirpath, dirnames, filenames in os.walk(pkg_name.replace('.', '/')):
            rel_dirpath = re.sub("^" + pkg_name + '/', '',  dirpath)
            # Ignore dirnames that start with '.'
            for i, dirname in enumerate(dirnames):
                if dirname.startswith('.'): del dirnames[i]
            if filenames:
                data_files += [os.path.join(rel_dirpath, f) for f in filenames
                               if re.search(EXT_PATTERN, f)]
        data_dict[pkg_name] = data_files
    return data_dict

v = file(os.path.join(os.getcwd(), 'jmb', 'core', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)
v.close()

setup(
    name='jmb.core',
    version = VERSION,
    description='jumbo 2 core', 
    long_description=long_description,
    author='ThunderSystems',
    url='http://hg.thundersystems.it/jmb/jmb.core',
    author_email='dev@thundersystems.it',
    packages=find_packages(exclude=['tests', 'tests.*']),
    platforms='any',
    zip_safe=False,
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Framework :: Django',
    ],
    test_suite = "jmb.core.tests",
    cmdclass={"test": TestRunner},
    install_requires = [
        'setuptools',
        'Django>=1.4.3',
        'jmb.i18n>=0.5.2',
        'jmb.l10n>=0.2.1',
        'South',
        'django-filter==0.7a0-sd8',
        'django-admin-tools==0.5.1-sd2',
        'django-tinymce==1.5.1b4-sd3',
        'xlwt',
        'xlrd',
        'django-autocomplete-light>=1.4.9,<1.9',
        'unicodecsv',
        'django-dajax-ng>=0.9.4',
        'django-dajaxice-ng>=0.5.6.5',
        'pyquery',
        'icalendar'
    ],
    namespace_packages = ['jmb'],    
    package_data=get_data_files('jmb.core')
)

