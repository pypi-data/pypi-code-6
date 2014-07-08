from distutils.core import setup
setup(
    name='easy_test',
    packages=['easy_test_selenium',
              'easy_test_selenium.commands',
              'easy_test_selenium.templates',
              'easy_test_selenium.templates.project',
              'easy_test_selenium.templates.project.principal',
              'easy_test_selenium.templates.test_name'],
    version='0.0.1',
    include_package_data=True,
    description='A python mini framework for tests that use Selenium',
    scripts=['bin/easy_test'],
    author='Carlos Huamani',
    author_email='carlos.hs.92@gmail.com',
    url='https://github.com/carloshs92/easy_test_selenium',
    download_url='https://github.com/carloshs92/easy_test_selenium/archive/master.zip',
    keywords=['test', 'functional test', 'selenium'],
    classifiers=[],
    install_requires=[
      'selenium>=2.42.1',
    ],
)

