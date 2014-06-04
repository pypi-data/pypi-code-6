# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

package_name = 'openslides-topicvoting'
module_name = 'openslides_topicvoting'

# The following commented unique string is used to detect this import.
module = __import__(module_name)  # Ro6Jaihaetahwex8eChohr3seeque5uovaehoyoo

with open('README.rst') as readme:
    long_description = readme.read()

with open('requirements.txt') as requirements:
    install_requires = requirements.readlines()

setup(
    name=package_name,
    version=module.__version__,
    description=module.__verbose_name__,
    long_description=long_description,
    author='Authors of %s, see AUTHORS' % module.__verbose_name__,
    author_email='openslides-topicvoting@normanjaeckel.de',
    url='https://github.com/normanjaeckel/openslides-topicvoting/',
    keywords='OpenSlides',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2'],
    license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={'openslides_plugins': '%s = %s' % (module.__verbose_name__, module_name)})
