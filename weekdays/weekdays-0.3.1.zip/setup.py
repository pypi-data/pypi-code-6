from setuptools import setup, find_packages

version = '0.3.1'

setup(name='weekdays',
      version=version,
      description="easily get business days of a range",
      long_description="""\
""",
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      keywords='date rrule weekdays business days',
      author='Florent Aide',
      author_email='florent.aide@gmail.com',
      url='http://bitbucket.org/xcg/weekdays',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          "python-dateutil",
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      tests_require=['nose', 'coverage'],
      )
