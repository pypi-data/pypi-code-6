import os

from setuptools import setup, find_packages

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'waitress',
    'launchkey-python'
]

test_requires = [
    'pyramid',
    'launchkey-python',
    'mocker'
]

setup(name='launchkey-pyramid',
      version='0.1',
      description='LaunchKey authentication extension for Pyramid',
      long_description=__doc__,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Brad Porter',
      url='https://github.com/LaunchKey/launchkey-pyramid',
      keywords='web pyramid pylons launchkey security authentication',
      license='MIT',
      packages=['pyramid_launchkey'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=test_requires,
      extras_require = {
        'launchkey_example':requires,
      },
      test_suite="pyramid_launchkey",
      entry_points="""\
      [paste.app_factory]
      launchkey_example = launchkey_example:main
      """,
      )
