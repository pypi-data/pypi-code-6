from setuptools import setup, find_packages
import treeeditor

setup(name='twentytab-treeeditor',
      version=treeeditor.__version__,
      description='A django app that provides FeinCMS admin tree editor.',
      author='20tab S.r.l.',
      author_email='info@20tab.com',
      url='https://github.com/20tab/twentytab-treeeditor',
      license='MIT License',
      install_requires=[
          'Django >=1.6',
          'django-appconf>=0.6',
      ],
      packages=find_packages(),
      include_package_data=True,
      package_data={
          '': ['*.html', '*.css', '*.js', '*.gif', '*.png', ],
      }
)
