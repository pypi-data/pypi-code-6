
import jingen_config
import logging
import logging.config
import os
import sys
from jinja2 import Environment, FileSystemLoader


DEFAULT_BASE_LOGGING_LEVEL = logging.INFO
DEFAULT_VERBOSE_LOGGING_LEVEL = logging.DEBUG

DEFAULT_VARS_FILE = 'vars.py'
DEFAULT_DOCKERFILE = 'Dockerfile'


def init_jingen_logger(base_level=DEFAULT_BASE_LOGGING_LEVEL,
                       verbose_level=DEFAULT_VERBOSE_LOGGING_LEVEL,
                       logging_config=None):
    """initializes a base logger

    you can use this to init a logger in any of your files.
    this will use config.py's LOGGER param and logging.dictConfig to configure
    the logger for you.

    :param int|logging.LEVEL base_level: desired base logging level
    :param int|logging.LEVEL verbose_level: desired verbose logging level
    :param dict logging_dict: dictConfig based configuration.
     used to override the default configuration from config.py
    :rtype: `python logger`
    """
    if logging_config is None:
        logging_config = {}
    logging_config = logging_config or jingen_config.LOGGER
    # TODO: (IMPRV) only perform file related actions if file handler is
    # TODO: (IMPRV) defined.

    log_dir = os.path.expanduser(
        os.path.dirname(
            jingen_config.LOGGER['handlers']['file']['filename']))
    if os.path.isfile(log_dir):
        sys.exit('file {0} exists - log directory cannot be created '
                 'there. please remove the file and try again.'
                 .format(log_dir))
    try:
        logfile = jingen_config.LOGGER['handlers']['file']['filename']
        d = os.path.dirname(logfile)
        if not os.path.exists(d) and not len(d) == 0:
            os.makedirs(d)
        logging.config.dictConfig(logging_config)
        jingen_lgr = logging.getLogger('user')
        # jingen_lgr.setLevel(base_level) if not jingen_config.VERBOSE \
        jingen_lgr.setLevel(base_level)
        return jingen_lgr
    except ValueError as e:
        sys.exit('could not initialize logger.'
                 ' verify your logger config'
                 ' and permissions to write to {0} ({1})'
                 .format(logfile, e))

jingen_lgr = init_jingen_logger()


def _set_global_verbosity_level(is_verbose_output=False):
    """sets the global verbosity level for console and the jingen_lgr logger.

    :param bool is_verbose_output: should be output be verbose
    """
    global verbose_output
    # TODO: (IMPRV) only raise exceptions in verbose mode
    verbose_output = is_verbose_output
    if verbose_output:
        jingen_lgr.setLevel(logging.DEBUG)
    else:
        jingen_lgr.setLevel(logging.INFO)
    # print 'level is: ' + str(jingen_lgr.getEffectiveLevel())


def _import_vars_file(vars_file):
    """returns a vars file object

    :param string vars_file: path to config file
    """
    # get config file path
    vars_file = vars_file or os.path.join(os.getcwd(), DEFAULT_VARS_FILE)
    jingen_lgr.debug('config file is: {}'.format(vars_file))
    # append to path for importing
    sys.path.append(os.path.dirname(vars_file))
    try:
        jingen_lgr.debug('importing vars file...')
        return __import__(os.path.basename(os.path.splitext(
            vars_file)[0])).VARS
    # TODO: (IMPRV) remove from path after importing
    except ImportError:
        jingen_lgr.warning('config file not found: {}.'.format(vars_file))
        raise JingenError('missing config file')
    except SyntaxError:
        jingen_lgr.error('config file syntax is malformatted. please fix '
                         'any syntax errors you might have and try again.')
        raise JingenError('bad config file')


class Jingen():

    def __init__(self, template_file,
                 vars_source=None,
                 output_file=None,
                 templates_dir=os.getcwd(),
                 make_file=False,
                 verbose=False):
        self.template_file = template_file
        self.vars_source = vars_source if type(vars_source) is dict \
            else _import_vars_file(vars_source)

        self.output_file = output_file if output_file else None
        self.templates_dir = templates_dir
        self.make_file = make_file
        _set_global_verbosity_level(verbose)

    def generate(self):
        """generates configuration files from templates using jinja2
        http://jinja.pocoo.org/docs/

        :param dict vars_source: contains the params to use
         in the template
        :param string output_file: output file path
        :param string template_file: template file name
        :param string templates_dir: template files directory
        """
        if type(self.vars_source) is not dict and \
                type(self.vars_source) is not str:
            jingen_lgr.error('vars_source must be a path or a dict')
            raise JingenError('vars_source must be a path or a dict')
        formatted_text = self._template_formatter()
        if self.make_file:
            self._make_file(formatted_text)
        return formatted_text

    def _template_formatter(self):
        """receives a template and returns a formatted version of it
        according to a provided variable dictionary
        """
        if type(self.templates_dir) is not str:
            raise JingenError('self.templates_dir must be of type string')
        if os.path.isdir(self.templates_dir):
            env = Environment(loader=FileSystemLoader(self.templates_dir))
        else:
            jingen_lgr.error('template dir missing: {0}'.format(
                self.templates_dir))
            raise JingenError('template dir missing')
        if type(self.template_file) is not str:
            raise JingenError('self.template_file must be of type string')
        if os.path.isfile(os.path.join(
                self.templates_dir, self.template_file)):
            template = env.get_template(self.template_file)
        else:
            jingen_lgr.error('template file missing: {0}'.format(
                self.template_file))
            raise JingenError('template file missing')

        try:
            jingen_lgr.debug('generating template from {0}/{1}'.format(
                self.templates_dir, self.template_file))
            return template.render(self.vars_source)
        except Exception as e:
            jingen_lgr.error('could not generate template ({0})'.format(e))
            raise JingenError('could not generate template')

    def _make_file(self, content):
        """creates a file from content

        :param string output_path: path to output the generated
         file to
        :param content: content to write to file
        """
        jingen_lgr.debug('creating file: {0} with content: \n{1}'.format(
            self.output_file, content))
        try:
            with open(self.output_file, 'w+') as f:
                f.write(content)
        except IOError:
            jingen_lgr.error('could not write to file')
            raise JingenError('could not write to file {0}'.format(
                self.output_file))


class JingenError(Exception):
    pass
