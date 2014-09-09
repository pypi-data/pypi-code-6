#!/usr/bin/python
# -*- coding: utf-8 -*-

# SàT: a XMPP client
# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014 Jérôme Poisson (goffi@goffi.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

try:
    from xdg import BaseDirectory
    from os.path import expanduser, realpath
except ImportError:
    BaseDirectory = None


class Const(object):

    ## Application ##
    APP_NAME = u'Salut à Toi'
    APP_NAME_SHORT = u'SàT'
    APP_NAME_FILE = u'sat'
    APP_NAME_FULL = u'%s (%s)' % (APP_NAME_SHORT, APP_NAME)
    APP_VERSION = u'0.5.0'  # Please add 'D' at the end for dev versions
    APP_URL = 'http://salut-a-toi.org'


    # Protocol
    XMPP_C2S_PORT = 5222


    ## Parameters ##
    NO_SECURITY_LIMIT = -1
    INDIVIDUAL = "individual"
    GENERAL = "general"
    # Parameters related to connection
    FORCE_SERVER_PARAM = "Force server"
    FORCE_PORT_PARAM = "Force port"
    # Parameters related to encryption
    PROFILE_PASS_PATH = ('General', 'Password')
    MEMORY_CRYPTO_NAMESPACE = 'crypto'  # for the private persistent binary dict
    MEMORY_CRYPTO_KEY = 'personal_key'
    # Parameters for static blog pages
    STATIC_BLOG_KEY = "Blog page"
    STATIC_BLOG_PARAM_TITLE = "Title"
    STATIC_BLOG_PARAM_BANNER = "Banner"
    STATIC_BLOG_PARAM_KEYWORDS = "Keywords"
    STATIC_BLOG_PARAM_DESCRIPTION = "Description"


    ## Menus ##
    MENU_GLOBAL = "GLOBAL"
    MENU_ROOM = "ROOM"
    MENU_SINGLE = "SINGLE"
    MENU_JID_CONTEXT = "JID_CONTEXT"
    MENU_ROSTER_JID_CONTEXT = "ROSTER_JID_CONTEXT"
    MENU_ROSTER_GROUP_CONTEXT = "MENU_ROSTER_GROUP_CONTEXT"


    ## Profile and entities ##
    PROF_KEY_NONE = '@NONE@'
    PROF_KEY_DEFAULT = '@DEFAULT@'
    ENTITY_ALL = '@ALL@'
    ENTITY_LAST_RESOURCE = 'LAST_RESOURCE'
    ENTITY_CAP_HASH = 'CAP_HASH'


    ## Messages ##
    MESS_TYPE_INFO = 'info'

    ## Configuration ##
    if BaseDirectory:  # skipped when xdg module is not available (should not happen in backend)

        ## Configuration ##
        DEFAULT_CONFIG = {
            'media_dir': '/usr/share/' + APP_NAME_FILE + '/media',
            'local_dir': BaseDirectory.save_data_path(APP_NAME_FILE),
            'pid_dir': '%(local_dir)s',
            'log_dir': '%(local_dir)s',
        }

        # List of the configuration filenames sorted by ascending priority
        CONFIG_FILES = [realpath(expanduser(path) + APP_NAME_FILE + '.conf') for path in
                        ['/etc/', '~/', '~/.', '', '.'] +
                        ['%s/' % path for path in list(BaseDirectory.load_config_paths(APP_NAME_FILE))]
                       ]


    ## Plugins ##
    # names of widely used plugins
    TEXT_CMDS = 'TEXT-COMMANDS'


    ## XMLUI ##
    XMLUI_WINDOW = 'window'
    XMLUI_POPUP = 'popup'
    XMLUI_FORM = 'form'
    XMLUI_PARAM = 'param'
    XMLUI_DIALOG = 'dialog'
    XMLUI_DIALOG_CONFIRM = "confirm"
    XMLUI_DIALOG_MESSAGE = "message"
    XMLUI_DIALOG_NOTE = "note"
    XMLUI_DIALOG_FILE = "file"
    XMLUI_DATA_ANSWER = "answer"
    XMLUI_DATA_CANCELLED = "cancelled"
    XMLUI_DATA_TYPE = "type"
    XMLUI_DATA_MESS = "message"
    XMLUI_DATA_LVL = "level"
    XMLUI_DATA_LVL_INFO = "info"
    XMLUI_DATA_LVL_WARNING = "warning"
    XMLUI_DATA_LVL_ERROR = "error"
    XMLUI_DATA_LVL_DEFAULT = XMLUI_DATA_LVL_INFO
    XMLUI_DATA_BTNS_SET = "buttons_set"
    XMLUI_DATA_BTNS_SET_OKCANCEL = "ok/cancel"
    XMLUI_DATA_BTNS_SET_YESNO = "yes/no"
    XMLUI_DATA_BTNS_SET_DEFAULT = XMLUI_DATA_BTNS_SET_OKCANCEL
    XMLUI_DATA_FILETYPE = 'filetype'
    XMLUI_DATA_FILETYPE_FILE = "file"
    XMLUI_DATA_FILETYPE_DIR = "dir"
    XMLUI_DATA_FILETYPE_DEFAULT = XMLUI_DATA_FILETYPE_FILE


    ## Logging ##
    LOG_BACKEND_STANDARD = 'standard'
    LOG_BACKEND_TWISTED = 'twisted'
    LOG_BACKEND_BASIC = 'basic'
    LOG_BACKEND_CUSTOM = 'custom'
    LOG_BASE_LOGGER = 'root'
    LOG_TWISTED_LOGGER = 'twisted'
    LOG_OPT_SECTION = 'DEFAULT' # section of sat.conf where log options should be
    LOG_OPT_PREFIX = 'log_'
    # (option_name, default_value) tuples
    LOG_OPT_COLORS = ('colors', 'true') # true for auto colors, force to have colors even if stdout is not a tty, false for no color
    LOG_OPT_LEVEL = ('level', 'info')
    LOG_OPT_FORMAT = ('fmt', '%(message)s') # similar to logging format.
    LOG_OPT_LOGGER = ('logger', '') # regex to filter logger name
    LOG_OPT_OUTPUT_SEP = '//'
    LOG_OPT_OUTPUT_DEFAULT = 'default'
    LOG_OPT_OUTPUT_MEMORY = 'memory'
    LOG_OPT_OUTPUT_MEMORY_LIMIT = 50
    LOG_OPT_OUTPUT_FILE = 'file' # file is implicit if only output
    LOG_OPT_OUTPUT = ('output', LOG_OPT_OUTPUT_SEP + LOG_OPT_OUTPUT_DEFAULT) # //default = normal output (stderr or a file with twistd), path/to/file for a file (must be the first if used), //memory for memory (options can be put in parenthesis, e.g.: //memory(500) for a 500 lines memory)
    LOG_LVL_DEBUG = 'DEBUG'
    LOG_LVL_INFO = 'INFO'
    LOG_LVL_WARNING = 'WARNING'
    LOG_LVL_ERROR = 'ERROR'
    LOG_LVL_CRITICAL = 'CRITICAL'
    LOG_LEVELS = (LOG_LVL_DEBUG, LOG_LVL_INFO, LOG_LVL_WARNING, LOG_LVL_ERROR, LOG_LVL_CRITICAL)


    ## HARD-CODED ACTIONS IDS (generated with uuid.uuid4) ##
    AUTHENTICATE_PROFILE_ID = u'b03bbfa8-a4ae-4734-a248-06ce6c7cf562'
    CHANGE_XMPP_PASSWD_ID = u'878b9387-de2b-413b-950f-e424a147bcd0'


    ## Text values ##
    BOOL_TRUE = "true"
    BOOL_FALSE = "false"


    ## Misc ##
    SAVEFILE_DATABASE = APP_NAME_FILE + ".db"
    IQ_SET = '/iq[@type="set"]'
    ENV_PREFIX = 'SAT_' # Prefix used for environment variables


    ## ANSI escape sequences ##
    # XXX: used for logging
    # XXX: they will be probably moved in a dedicated module in the future
    ANSI_RESET = '\033[0m'
    ANSI_NORMAL_WEIGHT = '\033[22m'
    ANSI_FG_BLACK, ANSI_FG_RED, ANSI_FG_GREEN, ANSI_FG_YELLOW, ANSI_FG_BLUE, ANSI_FG_MAGENTA, ANSI_FG_CYAN, ANSI_FG_WHITE = ('\033[3%dm' % nb for nb in xrange(8))
    ANSI_BOLD = '\033[1m'
    ANSI_BLINK = '\033[5m'
    ANSI_BLINK_OFF = '\033[25m'

    @classmethod
    def LOG_OPTIONS(cls):
        """Return options checked for logs"""
        # XXX: we use a classmethod so we can use Const inheritance to change default options
        return(cls.LOG_OPT_COLORS, cls.LOG_OPT_LEVEL, cls.LOG_OPT_FORMAT, cls.LOG_OPT_LOGGER, cls.LOG_OPT_OUTPUT)

    @classmethod
    def bool(cls, value):
        """retour str text value for bool, or bool value for str"""
        if isinstance(value, bool):
            return cls.BOOL_TRUE if value else cls.BOOL_FALSE
        return value.lower() == cls.BOOL_TRUE
