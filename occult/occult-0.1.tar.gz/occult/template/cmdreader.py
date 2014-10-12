# -*- coding: utf-8 -*-

from clint.textui import indent
from clint.textui import puts
from clint.textui import colored

class CommandReader(object):
    def __init__(self, options=None):
        self.options = options
        self.out = {}

        type = self.options.get('type', 'string')
        key = self.options.get('key')

        value = self.query()

        if self.validator(value):
            self.out[key] = value

    def query(self):
        title = self.options.get('title')
        default = self.options.get('default')
        type = self.options.get('type')
        ret = None

        if 'enum' in self.options:
            enum_value = None
            if 'enum_title' in self.options:
                puts(colored.green(self.options.get('enum_title','')+':'))
                for index, item in enumerate(self.options.get('enum', [])):
                    with indent(2):
                        puts('%d) %s' % (index+1, item.get('title')))
                    if item.get('value') == default:
                        enum_value = index

            q = raw_input('[%s] %s: %s ' % (colored.green('?'), title, ('(' + str(enum_value) + ')' if default else '')))

            if len(q) == 0:
                ret = default
            else:
                selected_index = int(q)
                selected_item = self.options.get('enum',[])[selected_index]
                ret = selected_item.get('value') if selected_item is not None else None
        else:
            ret = raw_input('[%s] %s: %s ' % (colored.green('?'), title, ('(' + str(default) + ')' if default else '')))
            if len(ret) == 0:
                ret = default

        if type=='int':
            ret = int(ret)
        elif type=='float':
            ret = float(ret)

        return ret

    def validator(self, value=None):
        required = self.options.get('required')
        return True
