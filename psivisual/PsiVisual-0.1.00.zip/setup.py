from distutils.core import setup

setup(
    name='PsiVisual',
    version='0.1.00',
    author='John Coady',
    author_email='johncoady@shaw.ca',
    packages=['psivisual', 'psivisual.test'],
    package_data={'psivisual': ['data/*.js']},
    url='http://pypi.python.org/pypi/PsiVisual/',
    license='LICENSE.txt',
    description='Test Stuff',
    long_description=open('README.txt').read(),
    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Natural Language :: English',
          'Programming Language :: Python :: 2.7',
          'Topic :: Multimedia :: Graphics :: 3D Modeling',
          'Topic :: Multimedia :: Graphics :: 3D Rendering',
          'Topic :: Scientific/Engineering :: Visualization',
    ],
)