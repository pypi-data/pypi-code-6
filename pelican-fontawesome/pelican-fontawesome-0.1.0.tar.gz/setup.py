from setuptools import setup, find_packages

version = __import__('pelican_fontawesome').__version__
download_url = 'https://github.com/kura/pelican-fontawesome/archive/{}.zip'.format(version)

setup(name='pelican-fontawesome',
      version=version,
      url='https://github.com/kura/pelican-fontawesome',
      download_url=download_url,
      author="Kura",
      author_email="kura@kura.io",
      maintainer="Kura",
      maintainer_email="kura@kura.io",
      description="Easily embed FontAwesome icons in your RST",
      long_description=open("README.rst").read(),
      license='MIT',
      platforms=['linux'],
      packages=find_packages(exclude=["*.tests"]),
      package_data={'': ['LICENSE', ]},
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: Implementation :: CPython',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Text Processing',
      ],
      zip_safe=True,
      )
