import os
from setuptools import setup

requirements = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'requirements.txt')

with open(requirements) as rf:
    requires = [l.strip() for l in rf.readlines()]

    setup(name='rstcv',
          author='Hung Nguyen Viet',
          author_email='hvn@familug.org',
          url='https://pypi.python.org/pypi/rstcv',
          version='0.1',
          scripts=['scripts/rstcv-build'],
          install_requires=requires,
          )
