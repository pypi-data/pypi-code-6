from distutils.core import setup
try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rest')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()


setup(
  name='opentuner',
  version='0.2.0',
  url='http://opentuner.org/',
  license='MIT',
  author='Jason Ansel',
  author_email='jansel@jansel.net',
  description='An extensible framework for program autotuning',
  long_description=read_md('README.md'),
  packages=['opentuner', 'opentuner.resultsdb', 'opentuner.utils',
            'opentuner.measurement', 'opentuner.search'],
)
