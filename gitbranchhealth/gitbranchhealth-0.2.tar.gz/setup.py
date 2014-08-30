from setuptools import setup
import os
import os.path

progName = 'gitbranchhealth'
progVersion = '0.2'
progDescription='A tool for determining the health of branches in a git repository',
progAuthor = 'Scott Johnson'
progEmail = 'jaywir3@gmail.com'
progUrl = 'http://github.com/jwir3/gitbranchhealth'
downloadUrl = 'https://github.com/jwir3/gitbranchhealth/archive/gitbranchhealth-v0.2.tar.gz',
entry_points = { 'console_scripts': [
  'git-branchhealth = gitbranchhealth.branchhealth:runMain',
]}
reqFilePath = "requirements.txt"
requirements_lines = [line.strip() for line in open(reqFilePath).readlines()]
installRequires = list(filter(None, requirements_lines))

setup(name=progName,
      version=progVersion,
      description=progDescription,
      author=progAuthor,
      author_email=progEmail,
      url=progUrl,
      packages=['gitbranchhealth'],
      entry_points=entry_points,
      test_suite='tests',
      install_requires=installRequires
)
