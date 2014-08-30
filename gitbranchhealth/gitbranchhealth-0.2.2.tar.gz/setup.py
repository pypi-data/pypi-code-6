from setuptools import setup
import os
import os.path

progName = 'gitbranchhealth'
progVersion = '0.2.2'
progDescription='A tool for determining the health of branches in a git repository',
progAuthor = 'Scott Johnson'
progEmail = 'jaywir3@gmail.com'
progUrl = 'http://github.com/jwir3/gitbranchhealth'
downloadUrl = 'https://github.com/jwir3/gitbranchhealth/archive/gitbranchhealth-v0.2.2.tar.gz',
entry_points = { 'console_scripts': [
  'git-branchhealth = gitbranchhealth.branchhealth:runMain',
]}
requirements = [
  'ansicolors>=1.0.2',
  'argparse>=1.2.1',
  'nicelog>=0.1.7',
  'GitPython>=0.3.2.RC1',
  'python-dateutil>=1.5'
]

curDir = os.path.dirname(os.path.realpath(__file__))

setup(name=progName,
      version=progVersion,
      description=progDescription,
      author=progAuthor,
      author_email=progEmail,
      url=progUrl,
      packages=['gitbranchhealth'],
      entry_points=entry_points,
      test_suite='tests',
      install_requires=requirements
)
