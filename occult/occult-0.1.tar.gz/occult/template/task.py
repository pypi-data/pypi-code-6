# -*- coding: utf-8 -*-

import os
import shutil
import codecs

import jinja2
from clint.textui import puts, colored,prompt

from .cmdreader import CommandReader


class Task(object):
    def __init__(self, options=None):
        self.options = options if options is not None else {}
        self.taskid = self.options.get('id')
        self.taskmanager = None
        self.nextTask = None
        self.out = {}

    def do_actions(self):
        pass

class CongfigureTask(Task):
    def do_actions(self):
        puts('[%s] Task Start.' % (colored.yellow(self.taskid)))
        steps = self.options.get('steps', None)
        preset = self.options.get('preset', None)
        configuration = None

        extra = self.taskmanager.extra
        if extra is not None and 'configuration' in extra:
            configuration = extra.get('configuration')

        if configuration is None:
            return

        configuration.update(preset)

        for option in steps:
            key = option.get('key')
            if key in configuration.data:
                option.update({'default':configuration.data.get(key)})
            step = CommandReader(option)
            self.out.update(step.out)

        configuration.data.update(self.out)
        is_ok = prompt.yn(colored.red('Attention!') + ' The configuration will be saved. Are you sure?')
        if is_ok:
            configuration.save()
            puts('[%s]%s configuration is saved.' % (colored.yellow(self.taskid), colored.green('SUCCESS!')))

            configuration.update({
                'pkg_path': os.path.dirname(configuration.path)
            })
            self.taskmanager.out[self.taskid] = configuration.data

            puts('[%s] Task Finished.' % (colored.yellow(self.taskid)))
            if self.nextTask is not None:
                self.nextTask.do_actions()
        else:
            return

class CopyTask(Task):
    def do_actions(self):
        puts('[%s] Task Start.' % (colored.yellow(self.taskid)))
        groups = self.options.get('files')
        files = []
        for group in groups:
            f = jinja2.Template(group.get('from','')).render(self.taskmanager.out)
            t = jinja2.Template(group.get('to','')).render(self.taskmanager.out)
            d = os.path.dirname(t)

            if not os.path.exists(d):
                os.makedirs(d)

            try:
                shutil.copy2(f,t)
                files.append(t)
                puts('[%s]%s %s cooy to %s' % (colored.yellow(self.taskid), colored.green('SUCCESS!'), f, t))
            except:
                puts('[%s]%s %s cooy to %s' % (colored.yellow(self.taskid), colored.red('FAILURE!'), f, t))

        self.out.update({
           'files':files
        })
        self.taskmanager.out[self.taskid] = self.out

        puts('[%s] Task Finished.' % (colored.yellow(self.taskid)))
        if self.nextTask is not None:
            self.nextTask.do_actions()

class RenderTask(Task):
    def do_actions(self):
        puts('[%s] Task Start.' % (colored.yellow(self.taskid)))

        options = self.options.get('options',{})
        source = options.get('source', None)
        target = options.get('target', None)
        files = []

        if source is not None and target is not None:
            source_path = jinja2.Template(source).render(self.taskmanager.out)
            target_path = jinja2.Template(target).render(self.taskmanager.out)
            env = jinja2.Environment(loader=jinja2.FileSystemLoader(source_path))
            groups = self.options.get('files')

            for group in groups:
                f = os.path.join(source_path, group.get('from'))
                t = jinja2.Template(group.get('to','')).render(self.taskmanager.out)

                try:
                    template = env.get_template(group.get('from'))
                    snippet = template.render(self.taskmanager.out)

                    puts('[%s]%s %s was rendered and copied to %s' % (colored.yellow(self.taskid), colored.green('SUCCESS!'), group.get('from'), os.path.relpath(t, target_path)))
                    d = os.path.dirname(t)

                    if not os.path.exists(d):
                        os.makedirs(d)

                    x = codecs.open(t, 'w+', encoding='utf-8')
                    x.write(snippet)
                    x.close()

                    files.append(t)
                except:
                    puts('[%s]%s %s was not rendered.' % (colored.yellow(self.taskid), colored.red('FAILURE!'), f))

        puts('[%s] Task Finished.' % (colored.yellow(self.taskid)))

