import urllib.parse
import tornado.gen
import tornado.web
import jazz


class NotesHandler(jazz.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        body = urllib.parse.parse_qs(self.request.body.decode())
        try:
            freq = (2 ** (1 / 12)) ** (int(body.get("n")[0]) - 49) * 440.0
        except ValueError:
            raise tornado.web.HTTPError(400)
        self.proc = tornado.process.Subprocess(
            "beep -f {:.1f}".format(freq), shell=True,
            stdin=tornado.process.Subprocess.STREAM,
            stdout=tornado.process.Subprocess.STREAM,
            stderr=tornado.process.Subprocess.STREAM)
        yield self.proc.stdout.read_until_close()
        status = self.proc.proc.wait()
        self.set_status(500 if status else 201)
