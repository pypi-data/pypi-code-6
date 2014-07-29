from setuptools import setup


try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ''

setup(name='comp-exp',
      version='2.0',
      description='Flexible computational experiments framework',
      long_description = long_description,
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='scientific computation experiment',
      url='https://hg.plav.in/my_projects/python/comp-exp',
      author='Alexander Plavin',
      author_email='alexander@plav.in',
      license='MIT',
      packages=['comp_exp', 'comp_exp.experimenters', 'comp_exp.experiments_data'],
      zip_safe=False)
