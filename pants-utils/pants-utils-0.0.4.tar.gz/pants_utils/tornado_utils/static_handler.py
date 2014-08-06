import pkg_resources
from os.path import join

from tornado.web import StaticFileHandler, HTTPError
from tornado import gen

class PexStaticFileHandler(StaticFileHandler):
    ''' 
    Utilizes the StaticFileHandler interface to serve static files
    from a (module, resource_path) directory. For example

    # Static content (CSS, js, etc.)
    (r'/static/(.*)', pants_utils.tornado_utils.PexStaticFileHandler,
    dict(path='my_module', subdir='static')),

    will server staticfiles from my_module/static    
    '''
    
    def initialize(self, path, default_filename=None, subdir=None):
        self.subdir = subdir
        return super(PexStaticFileHandler, self).initialize(path, default_filename)

    @gen.coroutine
    def get(self, path, include_body=True):
        if self.subdir:
            path = join(self.subdir, path)
        return super(PexStaticFileHandler, self).get(path, include_body)

    @classmethod
    def get_content(cls, abspath, start=None, end=None):
        '''Use package_resources to get string from resource.
           Abspath represents the <module>/<path>
        '''
        module = abspath.split("/")[0]
        path = join(*abspath.split("/")[1:])
        return pkg_resources.resource_string(module, path)

    def get_modified_time(self):
        return None

    @classmethod
    def get_absolute_path(cls, root, path):
        return join(root,path)

    def validate_absolute_path(self, root, absolute_path):
        module = absolute_path.split('/')[0]
        path = join(*absolute_path.split('/')[1:])

        if module != root:
            raise HTTPError(403, "%s is not in root static directory",
                            self.path)
        elif not pkg_resources.resource_exists(module, path):
            raise HTTPError(404)
        return absolute_path
