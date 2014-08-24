from distutils.core import setup

setup(
    name='django-fbrt',
    version='0.1.0',
    packages=['fbrt'],
    url='https://github.com/luismasuelli/facebook-realtime',
    license='GPL',
    author='Luis Masuelli',
    author_email='luismasuelli@hotmail.com',
    description='This package uses websockets and facebook API to let you create real-time application (e.g. a facebook-authenticated game). It is based on Fandjango and gevent/websockets using django-gevent-websocket. Readme is still pending. Sorry.',
    install_requires=[
        'Fandjango==4.2',
        'python-dateutil==2.2',
        'jsonfield==0.9.22',
        'django-gevent-websocket==0.1.0'
    ]
)
