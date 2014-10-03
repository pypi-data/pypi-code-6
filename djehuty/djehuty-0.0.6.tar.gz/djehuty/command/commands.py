# -*- coding: utf-8 -*-

from djehuty.command import Command


class Commands(Command):
    u'''show command list'''

    def take_action(self, parsed_args):
        app = self.app
        app.stdout.write(u'Commands:\n')
        command_manager = app.command_manager
        for name, ep in sorted(command_manager):
            try:
                factory = ep.load()
            except Exception as err:
                app.stdout.write(u'Could not load %r\n' % ep)
                continue
            try:
                cmd = factory(app, None)
            except Exception as err:
                app.stdout.write(u'Could not instantiate %r: %s\n' % (ep, err))
                continue
            one_liner = cmd.get_description().split(u'\n')[0]
            app.stdout.write(u'  %-13s  %s\n' % (name, one_liner))
