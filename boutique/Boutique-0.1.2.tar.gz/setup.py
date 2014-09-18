from setuptools import setup, find_packages


setup(
  name='Boutique',
  version='0.1.2',
  description="""
      The command line tool for boutiqueforge.com. It contains a web server
      embedded that can emulate the BoutiqueForge environment.
      This allows you to develop and test on your local machine before
      pushing any changes to online.

      More information at
      https://boutiqueforge.com/docs/article/getting_started
  """,

  packages=find_packages(),
  include_package_data=True,
  zip_safe=False,
  author='Boutiqueforge',
  author_email='hello@boutiqueforge.com',
  install_requires=['Flask==0.10.1',
                    'Jinja2==2.7.2',
                    'Flask-Script==0.5.3',
                    'requests==1.2.3',
                    'path.py==4.1',
                    'BoutiqueCommons==0.1.2'],
  entry_points={
      'console_scripts': ['boutique=boutiqueclient.boutique:main']
  },

)
