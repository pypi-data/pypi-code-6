import os
import sys
from jinja2 import Environment, FileSystemLoader

DEFAULT_VARS_FILE = 'vars.py'


def _import_vars_file(vars_file):
    """returns a vars file object

    :param string vars_file: path to config file
    """
    # get config file path
    vars_file = vars_file or os.path.join(os.getcwd(), DEFAULT_VARS_FILE)
    # append to path for importing
    sys.path.append(os.path.dirname(vars_file))
    try:
        return __import__(os.path.basename(os.path.splitext(
            vars_file)[0])).VARS
    # TODO: (IMPRV) remove from path after importing
    except ImportError:
        raise JingenError('missing config file')
    except SyntaxError:
        raise JingenError('bad config file')


class Jingen():

    def __init__(self, template_file,
                 vars_source=None,
                 output_file=None,
                 template_dir=os.getcwd(),
                 make_file=False):
        self.template_file = template_file
        self.vars_source = vars_source if type(vars_source) is dict \
            else _import_vars_file(vars_source)

        self.output_file = output_file if output_file else None
        self.template_dir = template_dir
        self.make_file = make_file

    def generate(self):
        """generates configuration files from templates using jinja2
        http://jinja.pocoo.org/docs/

        :param dict vars_source: contains the params to use
         in the template
        :param string output_file: output file path
        :param string template_file: template file name
        :param string template_dir: template files directory
        """
        if type(self.vars_source) is not dict and \
                type(self.vars_source) is not str:
            raise JingenError('vars_source must be a path or a dict')
        formatted_text = self._template_formatter()
        if self.make_file:
            self._make_file(formatted_text)
        return formatted_text

    def _template_formatter(self):
        """receives a template and returns a formatted version of it
        according to a provided variable dictionary
        """
        if type(self.template_dir) is not str:
            raise JingenError('template_dir must be of type string')
        if os.path.isdir(self.template_dir):
            env = Environment(loader=FileSystemLoader(self.template_dir))
        else:
            raise JingenError('template dir missing')
        if type(self.template_file) is not str:
            raise JingenError('template_file must be of type string')
        if os.path.isfile(os.path.join(
                self.template_dir, self.template_file)):
            template = env.get_template(self.template_file)
        else:
            raise JingenError('template file missing: {0}'.format(
                os.path.join(self.template_dir, self.template_file)))
        try:
            return template.render(self.vars_source)
        except Exception as e:
            raise JingenError('could not generate template: ({0}'.format(e))

    def _make_file(self, content):
        """creates a file from content

        :param string output_path: path to output the generated
         file to
        :param content: content to write to file
        """
        try:
            with open(self.output_file, 'w+') as f:
                f.write(content)
        except IOError:
            raise JingenError('could not write to file {0}'.format(
                self.output_file))


class JingenError(Exception):
    pass
