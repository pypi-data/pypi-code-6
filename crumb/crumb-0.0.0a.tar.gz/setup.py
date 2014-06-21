from setuptools import setup

setup(name = 'crumb',
    version = '0.0.0a',
    url = 'https://github.com/paulgb/crumb',
    description = 'Track arbitrary metrics across the git commits of a program',
    author = 'Paul Butler',
    author_email = 'paulgb@gmail.com',
    install_requires = [
        'pygit2>=0.20.3',
    ],
    packages = ['crumb'],
    entry_points = {
        'console_scripts': [
            'crumb = crumb.main:main',
            'git-crumb = crumb.main:main'
        ]
    },
)
