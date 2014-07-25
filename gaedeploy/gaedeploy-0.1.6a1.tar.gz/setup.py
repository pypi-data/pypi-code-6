from distutils.core import setup
from gaedeploy.version import get_version

setup(
    name = 'gaedeploy',
    packages = ['gaedeploy'],
    version = get_version("short"),
    description = 'Google AppEngine multi-environment deployment system',
    author = 'Nigel Dunn',
    author_email = 'nigel.dunn@gmail.com',
    url = 'https://github.com/nigeldunn/gaedeploy',
    download_url = 'https://github.com/nigeldunn/gaedeploy/tarball/' + get_version("short"),
    keywords = ['gae', 'deployment'],
    entry_points = {
        'console_scripts': [
            'gaed = gaedeploy.deploy:main',
        ]
    },
    classifiers = [
          'Development Status :: 1 - Planning',
          'Environment :: Console',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development',
          'Topic :: Software Development :: Build Tools',
    ],
)