from setuptools import setup, find_packages


version = '0.1.0'


setup(name="helga-hipster",
      version=version,
      description='Helga plugin to get hipster music recommendations',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Topic :: Communications :: Chat :: Internet Relay Chat',
          'Framework :: Twisted',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='helga music hipster',
      author='Shaun Duncan',
      author_email='shaun.duncan@gmail.com',
      url='https://github.com/shaunduncan/helga-hipster',
      license='MIT',
      install_requires=['requests==2.2.1'],
      packages=find_packages(),
      py_modules=['helga_hipster'],
      entry_points=dict(
          helga_plugins=[
              'hipster = helga_hipster:hipster'
          ],
      ),
)
