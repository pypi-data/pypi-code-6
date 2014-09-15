from setuptools import setup, find_packages

version = '1.1.2'

setup(name="helga-cowsay",
      version=version,
      description=('cowsay'),
      classifiers=[
          'Development Status :: 4 - Beta',
           'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
           'Operating System :: OS Independent',
           'Programming Language :: Python',
           'Topic :: Software Development :: Libraries :: Python Modules',
           'Topic :: Communications :: Chat :: Internet Relay Chat'],
      keywords='irc bot cow cowsay',
      author='Michael Orr',
      author_email='michael@orr.co',
      url='https://github.com/michaelorr/helga-cowsay',
      license='LICENSE',
      packages=find_packages(),
      include_package_data=True,
      py_modules=['helga_cowsay'],
      zip_safe=True,
      entry_points = dict(
          helga_plugins=[
              'cowsay= helga_cowsay:cowsay',
          ],
      ),
)
