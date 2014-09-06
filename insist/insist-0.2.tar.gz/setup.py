try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'insist',
    version = '0.2',
    author = 'Ray Harris',
    author_email = 'ray@harris.net',
    packages = [
      'insist',
    ],
    license='LICENSE',
    description='An easy-to-use assertion library for Python',
    long_description=open('README.md').read(),
    url='https://github.com/ray-harris-net/insist',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.2',
      'Programming Language :: Python :: 3.3',
      'Programming Language :: Python :: 3.4',
      'Intended Audience :: Developers',
      'License :: OSI Approved',
      'License :: OSI Approved :: Apache Software License',
      'Operating System :: OS Independent',
      'Topic :: Software Development',
      'Topic :: Software Development :: Testing',
      'Topic :: Software Development :: Libraries',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'Topic :: Utilities',
    ]
)
