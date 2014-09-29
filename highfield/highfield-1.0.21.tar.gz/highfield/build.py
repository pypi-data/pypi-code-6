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
    mkpath(loading.path('helpers'), module=True)
    mkpath(loading.path('views'))
    mkpath(loading.path('static/css/sources'))
    mkfile(loading.path('static/css/application.css'))
    mkpath(loading.path('static/js/'))
    mkfile(loading.path('static/js/application.js'))


    config = ("default_database_uri = None\n"
              "default_datbase_name = None\n"
              "session_secret_key = None\n\n"
              "routes = [('/static/<path:filepath>',\n"
              "           {'to': 'static.index',\n"
              "            'via': ['get']})]\n"
             )
    mkfile(loading.path('config.py'), config)

    static_controller = ("from highfield.base_controller import BaseController\n"
                         "\n"
                         "class StaticController(BaseController):\n"
                         "    def index(self, filepath):\n"
                         "        return self.static_file(filepath)\n"
                         "    pass\n"
                        )
    mkfile(loading.path('controllers/static_controller.py'), static_controller)

    server = ("from highfield.application import Application\n\n"
              "Application().run(network=True, debug=True)")
    mkfile(loading.path('server.py'), server)
    pass
