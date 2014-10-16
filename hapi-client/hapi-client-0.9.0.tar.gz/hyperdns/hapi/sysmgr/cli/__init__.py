"""HAPI CLI - Command Line Interface

to get started, type 'hapi'
"""

from hyperdns.hapi.sysmgr import SHAPI
import re
import os
import sys
import json
import base64
import getpass
import textwrap
import cmd

class SHAPICLI(SHAPI):
    """
    provides a simple wrapper around the hapi service, handling authentication
    and connection with a configuration file.
    """
    def dispatch(self,command):
        if command in SHAPICLI.command.registry.keys():
            self.command.registry[command](self.arguments,self)
        else:
            raise Exception('Command "%s" not found' % command)
            
    def __init__(self,arguments,docopt_doc=""):
        # note - we actually call the constructor in processArgs - this is bad, and should
        # be refactored.
        self.docopt_doc=docopt_doc
        self.processArgs(arguments)
        
    def processArgs(self,arguments):
        self.arguments=arguments
        
        # this will be set to 'True' if we need to configure, otherwise
        # it will be 
        self.config=self.read_config_or_exit()
        config=self.config
        
        # process the help command before we check for any configuration
        if arguments.get('help'):
            return self.dispatch('help')

        # run config if requested and before we check for any configuration
        elif config==None or arguments.get('config'):
            return self.dispatch('config')
            
        # load the config
        else:
            jwt=config['jwt']
            baseUrl=config['baseUrl']
            super(SHAPICLI,self).__init__(jwt,baseUrl)
            
            cmd=None
            for _cmd in arguments.keys():
                if _cmd.startswith("-") or _cmd.startswith("<"):
                    pass
                else:
                    if arguments[_cmd] and cmd==None:
                        cmd=_cmd
            
            return self.dispatch(cmd)


    def relogin(self):
        response=self.get('/auth/login',raw=True)
        self.jwt=response
        self.config['jwt']=self.jwt
        fname=self.config['fname']
        with open(fname,"w") as file:
            file.write(json.dumps(self.config, sort_keys=True, indent=4, separators=(',', ': ')))
            file.write('\n')
            return True
        return False

    class command(object):
    
        registry={}
        def __init__(self,oneline):
            self.oneline=oneline
    
        def __call__(self,f):
            f.oneline=self.oneline
            if f.__doc__==None:
                f.__doc__=''
            self.registry[f.__name__[4:]]=f
            return f



    def query_yes_no(self,question, default="yes"):
        """Ask a yes/no question via input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is one of "yes" or "no".
        """
        valid = {"yes":True,   "y":True,  "ye":True,
                 "no":False,     "n":False}
        if default == None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "\
                                 "(or 'y' or 'n').\n")
        

    def read_config_or_exit(self):
        """Read the config file.  If the --config=<path> option was provided on the
        command line, attempt to use that path.  If that option was not used, then
        check the env variable HAPI_CONFIG.  If present, attempt to read the
        config from that file.  Lastly, check for $HOME/.hapi and use that
        if it is present.  If a file can not be read, or if it is corrupt, then the
        system exits with the appropriate message.
        """
        try:
            arguments=self.arguments
            fname=arguments.get('--config')
            file=None
            if fname!=None:
                if os.access(fname,os.R_OK):
                    file=open(fname)
                else:
                    sys.exit('Config file %s is not readable.' % fname)
            else:
                if 'SHAPI_CONFIG' in os.environ:
                    fname=os.environ['HAPI_CONFIG']
                    if os.access(fname,os.R_OK):
                        file=open(fname)
                else:
                    if 'HOME' in os.environ:
                        fname="%s/.shapi" % (os.environ['HOME'])
                    if os.access(fname,os.R_OK):
                        file=open(fname)

            # allow 'hapi config' to run if no config file, and autoconfig if no config file
            if file==None and (arguments['config']!=None):
                print("Sorry, we can not find a valid config file.")
                print("  no config file via --config option")
                print("  no config.json in the cwd")
                print("  no HAPI_CONFIG environment variable")
                print("  no $HOME/.shapi file")
                print("------")
                if self.query_yes_no('Would you like to create $HOME/.shapi?'):
                    return None
                sys.exit('ok')

            try:
                config=json.loads(file.read())
            except Exception as e:
                print('Problem parsing config file %s, message=%s' % (fname,e))
                return None
            finally:
                file.close()

            assert 'jwt' in config.keys()
            assert 'baseUrl' in config.keys()
            config['fname']=fname
            return config
        except Exception as e:
            raise
            sys.exit('Failed to load config file: %s' % e)
    




