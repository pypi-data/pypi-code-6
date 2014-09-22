from setuptools import setup

setup(name='assemblycoins',
      version='0.1',
      author='Andrew Barisser',
      author_email='barisser@gmail.com',
      license='MIT',
      description='Digital Tokens on the Bitcoin Blockchain',
      packages=['assemblycoins'],
      install_requires=[
      'Flask',
      'Flask-SQLAlchemy',
      'MarkupSafe',
      'SQLAlchemy',
      'Werkzeug',
      'bitcoin',
      'ecdsa',
      'gunicorn',
      'itsdangerous',
      'psycopg2',
      'redis',
      'requests',
      'virtualenv',
      'wsgiref',
      'pytest',
      'Flask-Scss'
      ]
    )
