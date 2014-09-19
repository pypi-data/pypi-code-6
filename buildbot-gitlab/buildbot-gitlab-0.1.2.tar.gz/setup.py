import re
from distutils.core import setup

PYPI_RST_FILTERS = (
    # Replace code-blocks
    (r'\.\.\s? code-block::\s*(\w|\+)+', '::'),
    # Remove pypip.in badges
    (r'.*pypip\.in/.*', ''),
    (r'.*target: https://pypi.python.org/pypi/.*', ''),
)

def rst(filename):
    '''
    Load rst file and sanitize it for PyPI.
    '''
    filters = (
        # Replace code-blocks
        (r'\.\.\s? code-block::\s*(\w|\+)+',  '::'),
        # Remove pypip.in badges
        (r'.*pypip\.in/.*', ''),
        (r'.*target: https://pypi.python.org/pypi/.*', ''),
    )
    content = open(filename).read()
    for regex, replacement in filters:
        content = re.sub(regex, replacement, content)
    return content

long_description = '\n'.join((
    rst('README.rst'),
))

setup(
    name = 'buildbot-gitlab',
    packages = [    
        'buildbot.gitlab',
        'buildbot.gitlab.api',
        'buildbot.gitlab.monkey_patches',
        'buildbot.gitlab.monkey_patches.buildbot',
        'buildbot.gitlab.monkey_patches.buildbot.process',
        'buildbot.gitlab.monkey_patches.buildbot.process.build',
        'buildbot.gitlab.monkey_patches.buildbot.status',
        'buildbot.gitlab.monkey_patches.buildbot.status.progress'
    ],
    version = '0.1.2',
    description = 'Enhances a BuildBot installation to nicely integrate with GitLab',
    long_description = long_description,
    author = 'VCA Technology',
    author_email = 'info@vcatechnology.com',
    maintainer = 'Matt Clarkson',
    maintainer_email = 'matt.clarkson@vcatechnology.com',
    url = 'https://dev.vcatechnology.com/gitlab/tool-chain/buildbot-gitlab',
    keywords = ['continuous-integration', 'buildbot', 'gitlab'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Build Tools',
    ],
)

