import os
import json
from subprocess import Popen

from django.http import HttpResponse

from djangomaster.views import MasterView, JSONDetailView
from djangomaster.conf import settings


class TestRunner:

    def __init__(self):
        pass

    def run(self):
        pass


class TestView(MasterView):
    template_name = 'djangomaster/test.html'
    menu_item = 'test'

    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        context['cmd'] = self.request.GET.get('cmd', 'test')

        return context

    def get_queryset(self):
        return []


class ExecuteTestView(MasterView):

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(ExecuteTestView, self).get_context_data(**kwargs)
        context['cmd'] = self.request.GET.get('cmd', 'test')
        context['file_path'] = self._execute(context['cmd'])
        return context

    def _execute(self, cmd):
        cmd = ['python', 'manage.py'] + cmd.split(' ')
        file_path = os.path.join(settings.BASE_DIR, 'oi.txt')
        f = open(file_path, 'wr')
        Popen(cmd, stdout=f, stderr=f)
        return file_path

    def render_to_response(self, context):
        obj = {'file_path': 'oi.txt'}
        return HttpResponse(json.dumps(obj))


class CheckTestView(MasterView):

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(CheckTestView, self).get_context_data(**kwargs)
        return context

    def render_to_response(self, context):
        obj = {}
        obj['output'] = self._readfile()
        obj['finished'] = 'Destroying test database for alias' in obj['output']
        return HttpResponse(json.dumps(obj))

    def _readfile(self):
        file_path = os.path.join(settings.BASE_DIR, 'oi.txt')
        f = open(file_path, 'r')
        return f.read()
