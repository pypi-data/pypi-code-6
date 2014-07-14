from distutils.core import setup


setup(
    name='djhcup_reporting',
    version='0.20140714.1dev',
    description='Reporting module for the Django-HCUP Hachoir (djhcup)',
    #long_description=open('README.rst').read(),
    license='MIT',
    author='T.J. Biel',
    author_email='tbiel@med.umich.edu',
    packages=['djhcup_reporting'],
    provides=['djhcup_reporting'],
    classifiers=[
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
    ],
    requires=[
        'djhcup_core (>= 0.20140415)',
    ],
)
