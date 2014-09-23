from distutils.core import setup
 
setup(
    name='bigpanda-splunk',
    version=open('VERSION').read().replace("\n", ""),
    packages=['bigpanda_splunk'],
    license='apache v2',
    url="https://github.com/bigpandaio/bigpanda-splunk",
    description='BigPanda Splunk Action Script',
    author='BigPanda',
    author_email='support at bigpanda io',
    scripts=['bin/bigpanda-splunk', 'bin/bigpanda-splunk-configure', 'bin/bigpanda-splunk-defaults']
)
