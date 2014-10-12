import re
import jinja2
import codecs
import os
import shutil
import uuid
from pkg_resources import resource_string

from . import commentparser
from . import markdownparser


class Guide(object):
    matched_suffixes = set([
        '.scss', '.sass',
        '.less',
        '.css'
    ])
    def __init__(self, settingsobject):
        """
        Params:
            settingsobject (vitalstyles.settings.Settings): Settings.
        """
        self.settingsobject = settingsobject

    def iterfiles(self):
        for path in self.settingsobject['inpaths']:
            path = os.path.join(self.settingsobject.basedir, path)
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for filename in files:
                        if os.path.splitext(filename)[1] in self.matched_suffixes:
                            yield os.path.join(root, filename)
            else:
                yield path

    def _collect_comments(self):
        files = []
        for filepath in self.iterfiles():
            filecontent = codecs.open(filepath, 'rb', encoding='utf-8').read()
            parsedcomments = commentparser.Parse(filecontent)
            comments = []
            for comment in parsedcomments:
                comments.append(comment)
            files.append({
                'filepath': filepath,
                'relfilepath': os.path.relpath(filepath),
                'comments': comments
            })
        return files

    def render(self):
        templateloaders = [jinja2.PackageLoader('vitalstyles', 'templates')]
        if self.settingsobject.get_template_dir_path():
            templateloaders.insert(0, jinja2.FileSystemLoader(self.settingsobject.get_template_dir_path()))
        environment = jinja2.Environment(loader=jinja2.ChoiceLoader(templateloaders))
        environment.globals['settings'] = self.settingsobject
        environment.globals['uniquestamp'] = uuid.uuid1().hex
        
        markdownparser.StyleExampleBlockPreprocessor.set_jinja2_environment(environment)
        markdownparser.StyleExampleBlockPreprocessor.reset_isolated_file_counter()

        outdir = self.settingsobject.get_outdir_path()
        if os.path.exists(outdir):
            shutil.rmtree(outdir)
        os.makedirs(outdir)

        self.template = environment.get_template('index.html')
        rendered = self.template.render(files=self._collect_comments())
        rendered = re.sub(r'<div class="vitalstyles-reset vitalstyles-markdown">\s*</div>', '', rendered)

        with open(os.path.join(outdir, 'index.html'), 'wb') as f:
            f.write(rendered)

        outcss = os.path.join(outdir, 'styles.css')
        css = resource_string(__name__, 'styles/styles.css')
        with open(outcss, 'wb') as f:
            f.write(css)
