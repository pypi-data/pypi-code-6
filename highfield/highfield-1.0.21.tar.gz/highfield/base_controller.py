from flask import render_template, jsonify, redirect
from flask import url_for, send_from_directory
from flask import request, session

from highfield import naming

class MetaController(type):
    def __init__(cls, name, bases, clsdict):
        cls.canonical_name = naming.class_to_canonical(name)
        super(MetaController, cls).__init__(name, bases, clsdict)
        pass
    pass

class BaseController(object):
    __metaclass__ = MetaController

    def __init__(self, app, action):
        self.app = app
        self.action = action

        self.context = {}
        self.session = session
        self.cookies = request.cookies
        self.args = request.args
        self.form = request.form

        self.controllers = app.controllers
        self.models = app.models

        self.model = getattr(self.models, self.__class__.canonical_name, None)

        self.get = False
        self.post = False
        self.delete = False
        setattr(self, request.method.lower(), True)
        pass

    def uses(self, classname, action=None):
        cls = getattr(self.app.controllers, classname)
        return cls(self.app, action or self.action)

    def render(self, context=None, named_view=None, named_extension=None):
        if not named_view:
            folder_name = self.__class__.canonical_name
            file_name = self.action
            if not named_extension:
                named_extension = 'html'
                pass
            named_view = '%s/%s.%s' % (folder_name, file_name, named_extension)
            pass
        if context is not None:
            self.context.update(context)
        context = self.context
        return render_template(named_view, **context)

    def json(self, dictionary):
        return jsonify(**dictionary)

    def redirect(self, redirect_to, status_code=302):
        return redirect(redirect_to, status_code)

    def static_file(self, path):
        return send_from_directory(self.app.static_folder, path)

    def route_url(self, route):
        return url_for(route)
    pass
