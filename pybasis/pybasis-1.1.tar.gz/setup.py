from distutils.core import setup
from pip.req import parse_requirements


install_requirements = parse_requirements('requirements.txt')
requirements = [str(r) for r in install_requirements]

setup(name='pybasis',
      packages=['pybasis'],
      version='1.1',
      description='Unofficial python library for accessing the Basis API',
      author='Jay Weiler',
      author_email='jweiler@gmail.com',
      url='https://github.com/jayweiler/pybasis',
      download_url='https://github.com/jayweiler/pybasis/tarball/1.0',
      keywords=['basis'],
      classifiers=[],
      install_requires=requirements
    )
