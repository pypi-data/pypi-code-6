from distutils.core import setup
import pysteim
setup(
      name='pysteim',
      version=pysteim.__version__,
      author='Evgeniy Makhmudov',
      author_email='john_16@list.ru',
      url='bitbucket.org/john_16/pysteim',
      license='MIT',
      description='Support Steim algorithm in miniSEED',
      long_description='''Implementation of the algorithm Steim that used in miniSEED files. Support read Steim I and II, and write into STEM II. Also provide high level class miniSEED for reading miniSEED files.''',
      keywords=['Steim', 'miniSEED', 'MSEED', 'SEED'],
      platforms='OS Independent',
      classifiers=[
                   'Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2 :: Only',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Scientific/Engineering :: Physics'],
      py_modules=['pysteim']
      )