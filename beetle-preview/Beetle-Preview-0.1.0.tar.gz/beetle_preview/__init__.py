from beetle.renderers import MissingRendererError
from http import server
from socketserver import TCPServer
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from hashlib import md5
import os

class Updater(FileSystemEventHandler):
    def __init__(self, serve_directory, writer):
        self.basepath = os.getcwd()
        self.directory = serve_directory
        self.writer = writer
        self.cache = {}

    def on_any_event(self, event):
        # Urgh, ugly directory hack.
        # Could not find an easy way to serve files from a subfolder.
        os.chdir('..')
        for destination, content in self.writer.files():
            digest = md5(content).hexdigest()
            abs_path = os.path.join(
                self.basepath,
                self.directory,
                destination,
            )
            try:
                if destination not in self.cache:
                    self.writer.write_file(abs_path, content)
                    self.cache[destination] = digest
                    print('written', destination)
                elif self.cache[destination] != digest:
                        self.writer.write_file(abs_path, content)
                        self.cache[destination] = digest
                        print('updated', destination)
            except MissingRendererError:
                print('could not render:{}'.format(destination))
        os.chdir(self.directory)

class Server:
    def __init__(self, folders, output_folder, port, updater):
        self.directory = output_folder
        # self.content = content_folder
        self.folders = folders
        self.port = port
        self.updater = updater

    def monitor(self):
        observer = Observer()
        for each in self.folders:
            observer.schedule(self.updater, each, recursive=True)
        # observer.schedule(self.updater, self.content, recursive=True)
        observer.start()

    def serve(self):
        self.monitor()
        os.chdir(self.directory)

        request_handler = server.SimpleHTTPRequestHandler

        httpd = TCPServer(('', self.port), request_handler)
        try:
            print('Preview available at http://0.0.0.0:{}/'.format(self.port))
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()


def register(ctx, config):
    folders = [
        ctx.config.folders['content'],
        ctx.config.folders['include'],
        ctx.config.folders['templates'],
    ]
    # content_folder = ctx.config.folders['content']
    output_folder = ctx.config.folders['output']
    port = config.get('port', 5000)
    updater = Updater(ctx.config.folders['output'], ctx.writer)
    server = Server(folders, output_folder, port, updater)
    ctx.commander.add('preview', server.serve, 'Serve the rendered site')
