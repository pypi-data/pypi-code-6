from distutils.core import setup
import zebrapl

setup(name='ZebraPL',
      version=zebrapl.__version__,
      description='Zebra Programming Language II',
      author='Gamaliel Espinoza',
      author_email='gamaliel.espinoza@gmail.com',
      url='https://bitbucket.org/gamikun/zebrapl',
      packages=['zebrapl'],
      package_dir={'zebrapl' : 'zebrapl'}
)