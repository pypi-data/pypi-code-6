from setuptools import setup

setup(
  name = 'md2remark',
  py_modules = ['md2remark_runner'],
  packages = ['md2remark', 'md2remark.resources', 'md2remark.resources.templates'],
  package_data = {'md2remark.resources.templates': ['*.mustache']}, 
  install_requires = ['pystache==0.5.4'],
  version = '0.1.0',
  description = 'Builds a slideshow from markdown using remark.js.',
  long_description = open('README.rst', 'r').read(),
  author = 'Patrick Ayoup',
  author_email = 'patrick.ayoup@gmail.com',
  license = 'MIT',
  url = 'https://github.com/patrickayoup/md2remark/',
  download_url = 'https://github.com/patrickayoup/md2remark/tarball/0.1.0',
  keywords = ['markdown', 'slideshow'],
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Topic :: Utilities'
  ],
  entry_points = {
      'console_scripts': [
          'md2remark = md2remark_runner:run'
      ]
  },
)