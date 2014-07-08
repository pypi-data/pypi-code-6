import string
from easy_test_selenium.utils import render_templatefile, string_camelcase
import re, sys
from os.path import exists, join
import easy_test_selenium
import shutil
from shutil import copytree, ignore_patterns

TEMPLATES_PATH = join(easy_test_selenium.__path__[0], 'templates', 'project')
TEMPLATES_TO_RENDER = (
    ('manage.py'),
)
IGNORE = ignore_patterns('*.pyc', '.svn')

def run_command(name="principal"):
    if not re.search(r'^[_a-zA-Z]\w*$', name):
        print('Error: Project names must begin with a letter and contain only\n' \
            'letters, numbers and underscores')
        sys.exit(1)
    elif exists(name):
        print("Error: directory %r already exists" % name)
        sys.exit(1)

    moduletpl = join(TEMPLATES_PATH)
    copytree(moduletpl, name, ignore=IGNORE)
    shutil.copy(join(TEMPLATES_PATH, 'manage.py'), name)
    shutil.copy(join(TEMPLATES_PATH, 'principal', 'settings.py'), join(name, 'principal', 'settings.py'))
    for paths in TEMPLATES_TO_RENDER:
        path = join(paths)
        tplfile = join(name,
            string.Template(path).substitute(project_name=name))
        render_templatefile(tplfile, project_name=name,
            ProjectName=string_camelcase(name))
    print 'Project created successfully'