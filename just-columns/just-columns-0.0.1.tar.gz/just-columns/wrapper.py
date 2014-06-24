import tornado.web
import tornado.ioloop
import tornado.concurrent

import logging

path_maps = {
    
}

class get(object):
    def __init__(self, path, names=None):
        global path_maps

        self.path = path
        path_maps[path] = self
        self.function = None

        if names is None:
            names = []
        
        self.argument_names = names
        

        
    def __call__(self, *args, **kwargs):
        global path_maps

        if len(args) > 0:
            self.function = args[0]
                
        def funct(self_, *args, **kwargs):

            arguments = {name : self_.get_arguments(name) for name in self.argument_names}
            
            kwargs['arguments'] = arguments

            stuff = self.function(self_, *args, **kwargs)
            self_.write(stuff)

        path_maps[self.path] = funct
        return funct


def paths_to_handlers():
    global path_maps

    handlers = []

    for path, handler in path_maps.items():
        handler_class = type(
                            path + 'Handler', 
                            (tornado.web.RequestHandler, object), 
                            dict(get=handler)
        )


        handlers.append((path, handler_class))

    return handlers



def run(port_number=80):

    logging.info('Adding handlers')
    application = tornado.web.Application(paths_to_handlers())
    
    logging.info('Listening on port {}'.format(port_number))
    application.listen(port_number)

    logging.info('Main loop starting')
    tornado.ioloop.IOLoop.instance().start()
