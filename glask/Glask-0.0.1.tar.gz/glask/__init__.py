from flask import request, url_for
import flask


def current_for(**values):
    return url_for(request.endpoint, **values)


class Glask(flask.Flask):
    def __init__(self, import_name, static_path=None, static_url_path=None,
                 static_folder='static', template_folder='templates',
                 instance_path=None, instance_relative_config=False):
        super(Glask, self).__init__(import_name, static_path, static_url_path,
                                    static_folder, template_folder,
                                    instance_path, instance_relative_config)
        self.jinja_env.globals.update(current_for=current_for)