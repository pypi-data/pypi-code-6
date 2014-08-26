from subprocess import Popen, PIPE
import os

from django.conf import settings
from django.utils.importlib import import_module

from djangomaster.conf import settings as master_settings
from djangomaster.views import MasterView


class Result:

    def __init__(self, file_path, cmd=master_settings.PYLINT_CMD):
        self._path = file_path
        self._cmd = cmd
        self._result = ''

    @property
    def filename(self):
        index = len(master_settings.BASE_DIR) + 1
        return self._path[index:]

    @property
    def result(self):
        if not self._result:
            self._result = self.execute()
        return self._result

    def execute(self):
        cmd = [self._cmd, self._path]
        return Popen(cmd, stdout=PIPE).stdout.read()


class BaseLintView(MasterView):
    template_name = 'djangomaster/lint.html'
    context_object_name = 'results'
    menu_item = 'lint'
    lint_cmd = None
    lint_is_installed = False
    title = ''

    def is_valid_file(self, file_path):
        return True

    def lint(self, file_path):
        return Result(file_path, cmd=self.lint_cmd)

    def get_app_dirs(self):
        dirs = []
        for app in settings.INSTALLED_APPS:
            try:
                mod = import_module(app)
                dirs.append(mod.__path__[0])
            except ImportError:
                pass # What to do ?

        return dirs

    def get_files(self, dirname):
        ret = []

        for root, dirs, files in os.walk(dirname):
            for filename in files:
                file_path = os.path.join(root, filename)
                if self.is_valid_file(file_path):
                    ret.append(self.lint(file_path))

        return ret

    def get_queryset(self):
        ret = []
        if not master_settings.BASE_DIR:
            return ret

        dirs = sorted(self.get_app_dirs())
        for dirname in dirs:
            path = os.path.join(master_settings.BASE_DIR, dirname)
            if not dirname.startswith(master_settings.BASE_DIR):
                continue # to execute in only local code

            ret.extend(self.get_files(dirname))

        return ret

    def get_context_data(self, **kwargs):
        context = super(BaseLintView, self).get_context_data(**kwargs)
        context['page_title'] = self.title
        context['LINT_IS_INSTALLED'] = self.lint_is_installed
        context['LINT_CMD'] = self.lint_cmd
        return context


class PyLintView(BaseLintView):
    menu_item = 'pylint'
    lint_cmd = master_settings.PYLINT_CMD
    lint_is_installed = master_settings.PYLINT_IS_INSTALLED
    title = ''
    title = 'Py Lint'

    def is_valid_file(self, file_path):
        return file_path.endswith('.py')


class JsLintView(BaseLintView):
    menu_item = 'jslint'
    lint_cmd = master_settings.JSLINT_CMD
    lint_is_installed = master_settings.JSLINT_IS_INSTALLED
    title = 'JS Lint'

    def is_valid_file(self, file_path):
        return file_path.endswith('.js')

