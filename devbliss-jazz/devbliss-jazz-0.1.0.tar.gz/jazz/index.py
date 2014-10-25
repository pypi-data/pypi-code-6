import jazz


class IndexHandler(jazz.RequestHandler):

    def get(self):
        self.render("index.html")
