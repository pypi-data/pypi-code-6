from distutils.core import setup

setup(
    name = 'gaedeploy',
    packages = ['gaedeploy'],
    version = '0.1.3',
    description = 'Google AppEngine multi-environment deployment system',
    author = 'Nigel Dunn',
    author_email = 'nigel.dunn@gmail.com',
    url = 'https://github.com/nigeldunn/gaedeploy',
    download_url = 'https://github.com/nigeldunn/gaedeploy/tarball/0.1.3',
    keywords = ['gae', 'deployment', 'clemenger'],
    entry_points = {
        'console_scripts': [
            'gaed = gaedeploy.deploy:main',
        ]
    },
    classifiers = [],
)