from setuptools import setup

setup(
    name='kanc',
    description='Simple Kanboard CUI client',
    version='0.1.0',
    author="Yuichi Murata",
    author_email="yuichi1004@gmail.com",
    url = "https://github.com/yuichi1004/kanc",
    download_url = "https://github.com/yuichi1004/kanc/archive/v0.1.0.tar.gz",
    packages=['kanc', 'kanc.command'],
    install_requires = ['tabulate >= 0.7'],
    scripts=['scripts/kanc'],
    license="MIT"
    )

