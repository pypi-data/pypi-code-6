from .session import Session, SessionStorage
from .template import Loader, append_template_suffix
from .database import Connection

import codex.tornado.helpers
import tornado.websocket
import tornado.options
import tornado.ioloop
import tornado.escape
import tornado.web
import http.client
import functools
import traceback
import sys
import os

class Application(tornado.web.Application):
    def __init__(self, handlers=None, constants=None, **settings):
        self.constants = constants
        for arg_value in sys.argv:
            if arg_value.find('--port=') == 0:
                self.port = arg_value.replace('--port=', '', 1).strip()

        if not hasattr(self, 'port'):
            if 'default_port' in settings:
                self.port = settings['default_port']
            else:
                self.port = 80

        cli_args = [sys.argv[0]]
        self.root_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        if 'enable_logs' in settings and settings['enable_logs'] and 'log_path' in settings and settings['log_path']:
            settings['log_path'] = self.root_dir + '/' + settings['log_path'].strip('/') + '/'
            if not os.path.exists(settings['log_path']):
                os.mkdir(settings['log_path'])
            cli_args.append('--log_file_prefix=' + settings['log_path'] + 'port-' + str(self.port) + '.log')   

        if 'template_path' in settings:
            settings['template_path'] = self.root_dir + '/' + settings['template_path'].lstrip('/')

        if 'template_suffix' not in settings:
            settings['template_suffix'] = 'html'

        template_args = {}
        if 'autoescape' in settings:
            template_args['autoescape'] = settings['autoescape']
        settings['template_loader'] = Loader(settings['template_path'], **template_args)
        settings['template_loader'].set_template_suffix(settings['template_suffix'])

        if 'static_path' in settings:
            settings['static_path'] = self.root_dir + '/' + settings['static_path'].lstrip('/')

        if 'ui_methods' in settings:
            if isinstance(settings['ui_methods'], list):
                for i, ui_method in enumerate(settings['ui_methods']):
                    if isinstance(ui_method, str):
                        settings['ui_methods'][i] = __import__('app.helpers.' + ui_method)
                settings['ui_methods'].append(codex.tornado.helpers)
            else:
                raise Exception('ui_methods config must be a list')
        else:
            settings['ui_methods'] = [codex.tornado.helpers]

        if len(cli_args) > 1:
            tornado.options.parse_command_line(cli_args)

        super().__init__(handlers, **settings)

    def get_ioloop_instance(self):
        return tornado.ioloop.IOLoop.instance()
        
    def run(self):
        self.listen(self.port)
        tornado.ioloop.IOLoop.instance().start()

    def load_database(self):
        if not Connection.engine:
            if 'database' in self.settings and isinstance(self.settings['database'], dict):
                if 'debug' in self.settings['database']:
                    Connection.set_debug(self.settings['database']['debug'])
                Connection.set_engine(self.settings['database'])
            else:
                return None
        return Connection.create()

class ViewData(object):
    def __init__(self):
        self.__dict__['data'] = {}

    def __getattr__(self, name):
        return self.__dict__['data'].get(name)

    def __setattr__(self, name, value):
        self.__dict__['data'][name] = value

    def merge(self, data):
        self.__dict__['data'].update(data)
        return self

    def all(self):
        return self.__dict__['data']

class URI:
    def __init__(self, request_path):
        if request_path[0] == '/':
            request_path = request_path[1:]
        self.path = request_path
        self.segments = self.path.split('/')

    def segment(self, index, default=None):
        if index < 1:
            return None
        index -= 1
        if index >= len(self.segments):
            return default
        return self.segments[index]
        
class Controller(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        self._setup(application, request)
        super().__init__(application, request, **kwargs)
        self.disable_cache()

    def _setup(self, application, request, with_session=True):
        
        self.view = ViewData()
        self.request = request
        self.application = application
        self._models = {}

        if not hasattr(self, 'uri'):
            self.uri = URI(self.request.path)

        db_settings = self.application.settings.get('database')
        if db_settings and 'auto_init' in db_settings and db_settings['auto_init']:
            self.load_database()

        if with_session:
            sess_settings = self.application.settings.get('session')
            if sess_settings and 'auto_init' in sess_settings and sess_settings['auto_init']:
                self.load_session()
        
    def disable_cache(self):
        self.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Expires', '0')

    def load_database(self):
        if not hasattr(self, 'db'):
            self.db = self.application.load_database()

    def load_session(self):
        if hasattr(self, 'session'):
            return

        config = self.settings.get('session')
        if isinstance(config, dict) and config:

            if 'cookie_name' not in config or not config['cookie_name']:
                raise tornado.web.HTTPError(500, 'Cookie name for Session support must be defined')

            if not SessionStorage.engine:
                SessionStorage.set_engine(config)

            # if not SessionStorage.gc_activated:
            #     SessionStorage.set_gc(self.application.get_ioloop_instance(), 1000 * 3600)

            self.session = Session(self, config)

    def write_error(self, status_code, **kwargs):
        kwargs['code'] = status_code
        if 'exc_info' in kwargs:
            if self.settings.get('serve_traceback'):
                kwargs['message'] = '<pre>' + ''.join(traceback.format_exception(*kwargs['exc_info'])) + '</pre>'
            else:
                kwargs['message'] = kwargs['exc_info'][1]
        elif hasattr(self, '_reason'):
            kwargs['message'] = self._reason
        else:
            kwargs['message'] = http.client.responses[status_code]

        self.render('errors/' + str(status_code) + '.html', **kwargs)

    def get_argument(self, name, default=None, strip=True, xss_filter=None):
        return self._get_argument(name, default, self.request.arguments, strip, xss_filter)

    def get_query_argument(self, name, default=None, strip=True, xss_filter=None):
        return self._get_argument(name, default, self.request.query_arguments, strip, xss_filter)

    def get_body_argument(self, name, default=None, strip=True, xss_filter=None):
        return self._get_argument(name, default, self.request.body_arguments, strip, xss_filter)

    def _get_argument(self, name, default, source, strip=True, xss_filter=None):
        val = super()._get_argument(name, default, source, strip)
        if val and (xss_filter == True or (xss_filter is None and self.settings.get('global_xss_filtering'))):
            return tornado.escape.xhtml_escape(val)
        return val

    def get_arguments(self, name, strip=True, xss_filter=None):
        return self._get_arguments(name, self.request.arguments, strip, xss_filter)

    def get_query_arguments(self, name, strip=True, xss_filter=None):
        return self._get_arguments(name, self.request.query_arguments, strip, xss_filter)

    def get_body_arguments(self, name, strip=True, xss_filter=None):
        return self._get_arguments(name, self.request.body_arguments, strip, xss_filter)

    def _get_arguments(self, name, source, strip=True, xss_filter=None):
        values = super()._get_arguments(name, source, strip)
        if values and (xss_filter == True or (xss_filter is None and self.settings.get('global_xss_filtering'))):
            for k, v in enumerate(values):
                if v:
                    values[k] = tornado.escape.xhtml_escape(v)
        return values

    @property
    def constants(self):
        return self.application.constants

    @property
    def root_dir(self):
        return self.application.root_dir

    def view_exists(self, path):
        return os.path.exists(self.root_dir + '/app/views' + (('/' + path.lstrip('/')).rstrip('.') + '.') + self.settings.get('template_suffix'))

    def render_string(self, template_name, **kwargs):
        template_name = append_template_suffix(template_name, self.settings.get('template_suffix'))
        view_data = self.view.all()
        view_data.update(kwargs)
        view_data['constants'] = self.constants
        view_data['settings'] = self.settings
        if hasattr(self, 'uri'):
            view_data['uri'] = self.uri
        return super().render_string(template_name, **view_data)

    def load_form(self, name, formdata_fields=None, **kwargs):
        pos = name.rfind('.')
        package = '.' + name.lower()

        form = None
        try:
            form = getattr(__import__('app.forms' + package, fromlist=[name]), name)
        except ImportError:
            raise tornado.web.HTTPError(500, 'Form app.forms' + package + '.' + name + ' not found')
        except AttributeError:
            raise tornado.web.HTTPError(500, name + ' form not found in app.forms' + package)
        if form is None:
            return None

        xss_filter = None if 'xss_filter' not in kwargs else kwargs['xss_filter']
        if xss_filter is None:
            xss_filter = self.settings.get('global_xss_filtering')
        include_xss = [] if 'include_xss' not in kwargs else kwargs['include_xss']
        exclude_xss = [] if 'exclude_xss' not in kwargs else kwargs['exclude_xss']
        if formdata_fields is None:
            formdata_fields = self.request.arguments.keys()

        formdata = {}
        for field in formdata_fields:
            if (xss_filter and field not in exclude_xss) or (not xss_filter and field in include_xss):
                formdata[field] = self.get_argument(field, xss_filter=True)
            else:
                formdata[field] = self.get_argument(field, xss_filter=False)

        return form(self, formdata, **kwargs)

    def load_model(self, name):
        if not hasattr(self, 'db'):
            raise tornado.web.HTTPError(500, 'Database must be loaded first')

        loaded_model = self._models.get(name)
        if not loaded_model:

            package = '.' + name.lower()

            try:
                loaded_model = getattr(__import__('app.models' + package, fromlist=[name]), name)
            except ImportError:
                raise tornado.web.HTTPError(500, 'Model app.models' + package + '.' + name + ' not found')
            except AttributeError:
                raise tornado.web.HTTPError(500, name + ' model not found in app.models' + package)

            if loaded_model:
                loaded_model = loaded_model(self.db)
                self._models[name] = loaded_model

        return loaded_model

    def flash_cookie(self, name):
        value = self.get_cookie(name)
        if value is not None:
            self.clear_cookie(name)
        return value

    def flash_secure_cookie(self, name):
        value = self.get_secure_cookie(name)
        if value is not None:
            self.clear_cookie(name)
        return value
    
    def dispose_resources(self):
        if hasattr(self, 'db'):
            self.db.close()
            del self.db
        if hasattr(self, 'session'):
            self.session.save()
            del self.session

    def finish(self, chunk=None):
        super().finish(chunk)
        self.dispose_resources()

    def get_unauthenticated_url(self):
        return self.settings.get('unauthenticated_url')

class WebSocketController(tornado.websocket.WebSocketHandler, Controller):
    def __init__(self, application, request, **kwargs):
        self._setup(application, request, False)
        super().__init__(application, request, **kwargs)

    def on_connection_close(self):
        super().on_connection_close()
        self.dispose_resources()

for method in ["disable_cache", "flash_cookie", "flash_secure_cookie", "load_session"]:
    setattr(WebSocketController, method, tornado.websocket._wrap_method(getattr(WebSocketController, method)))

authenticated = tornado.web.authenticated

def unauthenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.current_user:
            url = self.get_unauthenticated_url()
            if url:
                self.redirect(url)
                return
            raise tornado.web.HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper

class Error(Controller):
    def __init__(self, application, request, status_code):
        super().__init__(application, request)
        self.set_status(status_code)
    
    def prepare(self):
        raise tornado.web.HTTPError(self._status_code)
 
tornado.web.ErrorHandler = Error