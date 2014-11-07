
import tornado.httpserver
import tornado.ioloop
import tornado.web
import os

class MainHandler(tornado.web.RequestHandler):

    def get(self):

        results = {'new':'thing', 'other':'thing'}
        self.render("main.html", results=results)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
           (r"/", MainHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()



if __name__ == "__main__":
    main()


