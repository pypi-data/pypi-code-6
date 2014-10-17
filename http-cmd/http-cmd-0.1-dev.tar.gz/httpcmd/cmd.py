from httpcmd.app import app
from flask import request
import json


class CmdHandler(object):

    def __init__(self, name, handler, required_args):
        self.name = name
        self.handler = handler
        self.required_args = required_args or {}

    def convert_args(self, args):
        for k in self.required_args:
            if k not in args:
                raise Exception('missing arg: `%s`' % k)
        return args

    def handle(self, args):
        return self.handler(**args)


class CmdManager(object):

    def __init__(self):
        self.handlers = {}

    def register(self, name, handler, required_args):
        self.handlers[name] = CmdHandler(name, handler, required_args)

    def handle(self, cmd_name):
        handler = self.handlers.get(cmd_name, None)
        if handler is None:
            raise Exception('unknown cmd: `%s`' % cmd_name)

        args = request.get_json() or {}
        args = handler.convert_args(args)
        return handler.handle(args)

cmd_mgr = CmdManager()


def register_cmd(*argv, name=None, required_args=None):
    def dec(handler):
        h_name = name or handler.__name__
        cmd_mgr.register(h_name, handler, required_args)
        return handler
    if argv:
        if len(argv) != 1:
            raise ValueError('invalid cmd handler')
        return dec(argv[0])
    return dec


@app.route('/cmd/<cmd>', methods=['POST'])
def cmd_handler(cmd):
    try:
        ret = cmd_mgr.handle(cmd)
    except Exception as e:
        ret = {'ok': False, 'errmsg': str(e)}

    if ret is None:
        ret = {'ok': True}
    return json.dumps(ret)
