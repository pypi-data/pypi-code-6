from highfield import loading
import os

def mkpath(path, module=False):
    try:
        os.makedirs(path)
        if module:
            mkfile(os.path.join(path, '__init__.py'), '')
        pass
    except OSError as e:
        if not os.path.isdir(path):
            raise
        pass
    pass

def mkfile(filename, content=''):
    with open(filename, 'w') as _file:
        _file.write(content)

def init():
    mkpath(loading.path('controllers'), module=True)
    mkpath(loading.path('models'), module=True)
    mkpath(loading.path('views'))
    mkpath(loading.path('static/css/sources'))
    mkfile(loading.path('static/css/application.css'))
    mkpath(loading.path('static/js/'))
    mkfile(loading.path('static/js/application.js'))

    config = ("mongodb_uri = \n"
              "db_name = \n"
              "\nroutes = \n"
             )
    mkfile(loading.path('config.py'), config)
    pass