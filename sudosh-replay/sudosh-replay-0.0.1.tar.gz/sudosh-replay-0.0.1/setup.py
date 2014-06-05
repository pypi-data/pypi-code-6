from setuptools import setup, find_packages
setup(
    name = 'sudosh-replay',
    version = '0.0.1',
    keywords=('sudosh','sudosh2','flask','TermRecord'),
    description='sudosh web replay',
    license = 'MIT License',
    install_requires = ['Flask==0.10.1','Flask-Login==0.2.11',
'Flask-OpenID==1.2.1',
'Flask-SQLAlchemy==1.0',
'Flask-WTF==0.9.5',
'Flask-WhooshAlchemy==0.55',
'Jinja2==2.7.2',
'MarkupSafe==0.23',
'SQLAlchemy==0.9.4',
'Tempita==0.5.3dev',
'WTForms==1.0.5',
'Werkzeug==0.9.4',
'Whoosh==2.6.0',
'blinker==1.3',
'decorator==3.4.0',
'flup==1.0.3.dev-20110405',
'itsdangerous==0.24',
'pbr==0.8.2',
'pysqlite==2.6.3',
'python-openid==2.2.5',
'six==1.6.1',
'sqlalchemy-migrate==0.9.1',
'virtualenv==1.9.1',
'wsgiref==0.1.2',],
    author = 'zhailibao2013',
    author_email ='zhailibao2013@aliyun.com',
    packages = find_packages(),
    platforms = 'any',
)
