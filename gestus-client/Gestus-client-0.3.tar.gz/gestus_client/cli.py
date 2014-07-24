# -*- coding: utf-8 -*-
"""
Command line action
"""
import datetime, os

from requests.exceptions import HTTPError, ConnectionError, InvalidSchema

from argh import arg, ArghParser
from argh.exceptions import CommandError

from gestus_client import logging_handler
from gestus_client import __version__ as client_version
from gestus_client.config import GestusConfig
from gestus_client.client import GestusClient, WebsitePostException, ENVIRONMENT_KIND_CHOICES, ENVIRONMENT_KIND_KEYS


# Available common options for all commands
cmd_user_opt = arg('-u', '--user', default=None, help="Username to connect to the service")
cmd_password_opt = arg('-p', '--password', default=None, help="Password to connect to the service")
cmd_host_opt = arg('-o', '--host', default=None, help="Http(s) address to connect to the service")
cmd_config_opt = arg('-c', '--config', default='gestus.cfg', help="Path to the client config file")
cmd_passive_opt = arg('--passive', default=False, action='store_true', help="Disable config saving")
cmd_loglevel_opt = arg('-l', '--loglevel', default='info', choices=['debug','info','warning','error','critical'], help="The minimal verbosity level to limit logs output")
cmd_logfile_opt = arg('--logfile', default=None, help="A filepath that if setted, will be used to save logs output")
cmd_timer_opt = arg('-t', '--timer', default=False, action='store_true', help="Display elapsed time at the end of execution")
cmd_eggs_opt = arg('-g', '--eggs', default=None, help="Path to the eggs directory to scan")
cmd_websitename_opt = arg('--name', default=None, help="Website name")
cmd_websiteurl_opt = arg('--url', default=None, help="Environnment url")
cmd_websiteenv_opt = arg('--env', default=None, choices=ENVIRONMENT_KIND_KEYS, help="Environnment name")
cmd_websiteserver_opt = arg('--server', default=None, help="Environnment server address/hostname")


class CliInterfaceBase(object):
    """
    The common base CLI interface to use within a command function
    
    It takes care of the logging, timer, config and service connection, also embed some common args validate
    """
    def __init__(self, args):
        self.args = args
        
        self.config = None
        self.con = None
        
        self.starttime = datetime.datetime.now()
        # Init, load and builds
        self.root_logger = logging_handler.init_logging(self.args.loglevel.upper(), logfile=self.args.logfile)
    
    def open_config(self):
        # Open config file if exists
        self.config = GestusConfig()
        self.config.open(self.args.config)
        configdatas = self.config.get_datas()
        # Merge config in arguments for empty argument only
        for item in GestusConfig.options:
            if item in configdatas:
                val = getattr(self.args, item, None) or configdatas[item]
                setattr(self.args, item, val)
                self.root_logger.debug("Set config value '%s' to: %s", item, val)
    
    def save_config(self):
        # Save config with current values
        if self.config and not self.args.passive:
            self.root_logger.debug("Saving config")
            values = {}
            for item in GestusConfig.options:
                if hasattr(self.args, item):
                    values[item] = getattr(self.args, item)
            
            self.config.set_datas(values)
            self.config.save()
    
    def connect(self):
        """
        Connect to the PO Project API service
        """
        # Open client
        self.con = GestusClient(self.args.host, (self.args.user, self.args.password))
        
        # Connect to the service
        try:
            self.con.connect()
        except (HTTPError, ConnectionError, InvalidSchema) as e:
            import traceback
            top = traceback.extract_stack()[-1]
            self.root_logger.error("%s: %s", type(e).__name__, e)
            raise CommandError('Error exit')
    
    def close(self):
        if self.args.timer:
            endtime = datetime.datetime.now()
            self.root_logger.info('Done in %s', str(endtime-self.starttime))
    
    def validate_authentication_args(self):
        # Validate required arguments to connect
        if not self.args.user or not self.args.password or not self.args.host:
            self.root_logger.error("'user', 'password' and 'hostname' are required arguments to connect to the service")
            raise CommandError('Error exit')
    
    def validate_website_args(self):
        # Validate required argument to register
        if not self.args.name or not self.args.url or not self.args.env:
            self.root_logger.error("'name', 'url' and 'env' are required arguments to register the current environment")
            raise CommandError('Error exit')
    
    def validate_eggs_args(self):
        # Validate eggs path argument
        if self.args.eggs and not os.path.exists(self.args.eggs):
            self.root_logger.error("The given eggs path does not exists")
            raise CommandError('Error exit')
        if self.args.eggs and not os.path.isdir(self.args.eggs):
            self.root_logger.error("The given eggs path is not a directory")
            raise CommandError('Error exit')
    
    def validate_env_args(self):
        # Validate environment kind
        if self.args.env not in ENVIRONMENT_KIND_KEYS:
            self.root_logger.error("Invalid environment given '%s'. Valid choices are: %s", self.args.env, ', '.join(ENVIRONMENT_KIND_KEYS))
            raise CommandError('Error exit')
    
    def validate_url_args(self):
        # Validate url
        if self.args.url.find(' ') > -1:
            self.root_logger.warning("Seems you tried to define multiple url separated with spaces, Gestus only accepts one url for an environment, the value has been splitted to get the first one item")
            self.args.url = self.args.url.split(' ')[0]


@cmd_user_opt
@cmd_password_opt
@cmd_host_opt
@cmd_config_opt
@cmd_passive_opt
@cmd_loglevel_opt
@cmd_logfile_opt
@cmd_timer_opt
@cmd_eggs_opt
@cmd_websitename_opt
@cmd_websiteurl_opt
@cmd_websiteenv_opt
@cmd_websiteserver_opt
def register(args):
    """
    Register current environment
    """
    interface = CliInterfaceBase(args)
    
    interface.open_config()
    
    interface.validate_authentication_args()
    interface.validate_website_args()
    interface.validate_eggs_args()
    interface.validate_env_args()
    interface.validate_url_args()
    
    interface.connect()
    
    # Register meta datas
    register_args = [interface.args.name, interface.args.url, interface.args.env]
    if interface.args.server:
        register_args.append(interface.args.server)
    try:
        interface.args.website_id, interface.args.environment_id = interface.con.register(*register_args)
    except WebsitePostException as e:
        interface.root_logger.error(e)
        raise CommandError('Error exit')
    
    # Update server host for saving in config file
    interface.args.server = interface.con.environment_server
        
    # Register egg list
    if interface.args.eggs:
        try:
            interface.con.register_eggs(interface.args.eggs)
        except WebsitePostException as e:
            interface.root_logger.error(e)
            raise CommandError('Error exit')
    
    interface.save_config()
    interface.close()


@cmd_user_opt
@cmd_password_opt
@cmd_host_opt
@cmd_config_opt
@cmd_passive_opt
@cmd_loglevel_opt
@cmd_logfile_opt
@cmd_timer_opt
@cmd_eggs_opt
@cmd_websitename_opt
@cmd_websiteurl_opt
@cmd_websiteenv_opt
@cmd_websiteserver_opt
def update(args):
    """
    TODO: Update current environment
    """
    starttime = datetime.datetime.now()
    # Init, load and builds
    root_logger = logging_handler.init_logging(args.loglevel.upper(), logfile=args.logfile)
    
    print "Hello world!"
    
    if args.timer:
        endtime = datetime.datetime.now()
        root_logger.info('Done in %s', str(endtime-starttime))

def main():
    """
    Main entrypoint for console_script (commandline script)
    """
    parser = ArghParser()
    parser.add_argument('-v', '--version', action='version', version=client_version)
    enabled_commands = [register]
    
    parser.add_commands(enabled_commands)
    parser.dispatch()
