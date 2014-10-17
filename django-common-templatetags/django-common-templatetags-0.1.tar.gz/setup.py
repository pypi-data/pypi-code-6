from setuptools import setup

setup(
    name='django-common-templatetags',
    version = '0.1',
    description='Common templatetags missing for application',
    author='aRkadeFR',
    author_email='contact@arkade.info',
    url='https://github.com/aRkadeFR/django-common-templatetags',
    package_dir = {'': 'project'},
    packages = ['common_templatetags'],
    classifiers = [
        'Framework :: Django',
    ],
    # test_suite = 'your.module.tests',
    #use_2to3 = True,
    #convert_2to3_doctests = ['src/your/module/README.txt'],
    #use_2to3_fixers = ['your.fixers'],
    #use_2to3_exclude_fixers = ['lib2to3.fixes.fix_import'],
)
