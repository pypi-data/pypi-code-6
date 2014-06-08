import re
import markdown
import os
from markdown.extensions import Extension
from markdown.extensions import codehilite


class StyleExampleExtension(Extension):
    def __init__(self, configs):
        # define default configs
        self.config = {
            'settings': [None, "vitalstyles.settings.Settings object."],
        }

        # Set config
        self.setConfig('settings', configs['settings'])


    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.preprocessors.add('vitalstyles_example_block',
            StyleExampleBlockPreprocessor(md, settingsobject=self.config['settings'][0]),
            ">normalize_whitespace")



class StyleExampleBlockPreprocessor(markdown.preprocessors.Preprocessor):
    FENCED_BLOCK_RE = re.compile(r'''
(?P<fence>^\${3,})[ ]*         # Opening $$$
(?:(?P<examplestyle>isolated|fullwidth)?[ ]*\n)
(?P<html>.*?)(?<=\n)
(?P=fence)[ ]*$''', re.MULTILINE | re.DOTALL | re.VERBOSE)

    codehilite_lang = 'html'


    @classmethod
    def set_jinja2_environment(cls, environment):
        cls.jinja2_environment = environment

    @classmethod
    def reset_isolated_file_counter(cls):
        cls.isolated_file_counter = 0

    @classmethod
    def get_next_isolated_preview_filename(cls):
        counter = cls.isolated_file_counter
        cls.isolated_file_counter += 1
        return 'preview.{}.html'.format(counter)

    def __init__(self, md, settingsobject):
        super(StyleExampleBlockPreprocessor, self).__init__(md)
        self.checked_for_codehilite = False
        self.settingsobject = settingsobject
        self.codehilite_conf = {
            'lang': self.codehilite_lang
        }

    def _render_jinja2_template(self, template_name, **render_kwargs):
        template = self.__class__.jinja2_environment.get_template(template_name)
        return template.render(**render_kwargs).strip()

    def run(self, lines):
        """ Match and store Example Code Blocks in the HtmlStash. """

        # Check for html hilite extension
        if not self.checked_for_codehilite:
            for ext in self.markdown.registeredExtensions:
                if isinstance(ext, codehilite.CodeHiliteExtension):
                    self.codehilite_conf = ext.config.copy()
                    # self.codehilite_conf['lang'] = self.codehilite_lang
                    # if 'force_linenos' in self.codehilite_conf:
                    #     # force_linenos is deprecated and does not work with
                    #     # the CodeHilite class. I guess it is converted to
                    #     # the ``linenums`` option in the extension.
                    #     del self.codehilite_conf['force_linenos']
                    # if 'pygments_style' in self.codehilite_conf:
                    #     del self.codehilite_conf['pygments_style']
                    break

            self.checked_for_codehilite = True

        text = "\n".join(lines)
        while 1:
            m = self.FENCED_BLOCK_RE.search(text)
            if m:
                html = m.group('html')
                examplestyle = m.group('examplestyle')
                if examplestyle is None:
                    examplestyle = 'default'
                previewfilename = self._save_htmlfile(html, examplestyle)
                rendered = self._render_examplehtml(html, examplestyle, previewfilename)
                placeholder = self.markdown.htmlStash.store(rendered, safe=True)
                text = '%s\n%s\n%s'% (text[:m.start()], placeholder, text[m.end():])
            else:
                break

        return text.split("\n")

    def _save_htmlfile(self, html, examplestyle):
        if examplestyle == 'isolated':
            unique_filename = self.__class__.get_next_isolated_preview_filename()
            with open(os.path.join(self.settingsobject['outdir'], unique_filename), 'wb') as f:
                preview = self._render_jinja2_template('preview-standalone.html',
                    html=html)
                f.write(preview)
            return unique_filename
        else:
            return None

    def _render_examplehtml(self, html, examplestyle, previewfilename):
        codeblock = self._render_hilighted_codeblock(html)
        previewblock = self._render_previewblock(html, examplestyle, previewfilename)
        return self._render_jinja2_template('example.html',
            examplestyle=examplestyle,
            codeblock=codeblock,
            previewblock=previewblock)

    def _render_hilighted_codeblock(self, html):
        highliter = codehilite.CodeHilite(html,
            lang=self.codehilite_lang,
            noclasses=self.codehilite_conf.get('noclasses', [True, None])[0]
        )
        return highliter.hilite()

    def _render_previewblock(self, html, examplestyle, previewfilename):
        return self._render_jinja2_template(
            'preview-{}.html'.format(examplestyle),
            html=html,
            examplestyle=examplestyle,
            previewfilename=previewfilename)

    def _escape(self, txt):
        """ basic html escaping """
        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        return txt




def to_html(input_markdown, settingsobject):
    codehilite_conf = {
        'linenums': False,
        'noclasses': True
    }
    md = markdown.Markdown(
        output_format='html5',
        safe_mode="escape",
        extensions=[
            'codehilite', # Syntax hilite code
            'fenced_code', # Support github style code blocks
            'sane_lists', # Break into new ul/ol tag when the next line starts with another class of list indicator
            'smart_strong', # Do not let hello_world create an <em>,
            'def_list', # Support definition lists
            'tables', # Support tables
            'smarty',
            StyleExampleExtension(configs={'settings': settingsobject}),
        ],
        extension_configs={
            'codehilite': codehilite_conf
        })
    return u'<div class="vitalstyles-reset vitalstyles-markdown">{}</div>'.format(md.convert(input_markdown))