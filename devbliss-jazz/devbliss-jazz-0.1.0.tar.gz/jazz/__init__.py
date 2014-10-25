import pkg_resources
import tornado.web
import tornado.util


__version__ = pkg_resources.get_distribution("devbliss-jazz").version


class RequestHandler(tornado.web.RequestHandler):

    pass


class ErrorHandler(RequestHandler, tornado.web.ErrorHandler):

    pass


class Application(tornado.web.Application):

    handlers = [
        ("/", tornado.util.import_object(
            "jazz.index.IndexHandler")),
        ("/notes", tornado.util.import_object(
            "jazz.notes.NotesHandler")),
        (".*", ErrorHandler, {"status_code": 404})
    ]

    settings = {
        "template_path": pkg_resources.resource_filename(
            "jazz", "templates"),
        "static_path": pkg_resources.resource_filename(
            "jazz", "static"),
    }

    def __init__(self, **kwargs):
        self.settings.update(kwargs)
        super().__init__(self.handlers, **self.settings)
