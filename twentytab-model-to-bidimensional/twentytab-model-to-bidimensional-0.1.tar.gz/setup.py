from setuptools import setup, find_packages
import bidimensional

setup(name='twentytab-model-to-bidimensional',
      version=bidimensional.__version__,
      description='A django app that returns a bidimensional representation of a given model and queryset following foreign keys recursively',
      author='20tab S.r.l.',
      author_email='info@20tab.com',
      url='https://github.com/20tab/twentytab-model-to-bidimensional',
      license='MIT License',
      packages=find_packages(),
      include_package_data=True,
      package_data={
          '': ['*.html', '*.css', '*.js', '*.gif', '*.png', ],
      }
)
