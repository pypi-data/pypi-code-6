from setuptools import setup, find_packages


version = '0.1.0'


setup(name="helga-flip",
      version=version,
      description=('Helga plugin to flip words'),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Topic :: Communications :: Chat :: Internet Relay Chat',
          'Framework :: Twisted',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='helga flip',
      author='Shaun Duncan',
      author_email='shaun.duncan@gmail.com',
      url='https://github.com/shaunduncan/helga-flip',
      license='GPLv3',
      packages=find_packages(),
      py_modules=['helga_flip'],
      entry_points = dict(
          helga_plugins=[
              'flip = helga_flip:flip'
          ],
      ),
)
