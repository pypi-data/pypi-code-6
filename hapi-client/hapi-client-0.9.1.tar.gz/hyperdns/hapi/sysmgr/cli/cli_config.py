from hyperdns.hapi.sysmgr.cli import SHAPICLI
import readline
import getpass
import os
import json

def rlinput(prompt, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()

@SHAPICLI.command('Configure the environment with your hapi email, password and host')
def cmd_config(arguments,hapi):
    """config
    
    Run an interactive script to generate the config.
    
    The config will be tested and you will have the option to save the config
    if it works.
    
    this program will look for config as follows:
       - look at a path if --config=<path> is provided
       - look for the env variable HAPI_CONFIG and use that path if present
       - attempt to load a file from $HOME/.hapi
       
    The format of the config file is as follows
        {
            "base":"..... server url ......",
            "username":"your email",
            "password":"your password"
        }
        
        
    Example Invocations
        config
            Run an interactive shell to configure your client
            .
            Example Output:
                (zup-server)dnsmanager:zup-server $ d config
                Base Url: http://localhost:5000
                Email: zork@place.com
                Password: 
                Would you like to save to [Y/N]? Y 
                Saved config in /Users/dnsmanager/.hapi
    """
    config=hapi.config
    
    config_map={
        "baseUrl":('Base Url','http://localhost:5000/my'),
        "specUrl":('Client Specification Url','http://localhost:5000/client/model/python'),
        "jwt":('JWT (Empty if you want to generate one)','')
        }
    if config==None or config==True:
        config={}
    
    print("\nWelcome to the HAPI configurator!\n")
    for key in sorted(config_map.keys()):
        (label,default_value)=config_map[key]
        if key not in config.keys():
            config[key]=default_value
        label="\033[%sm%s\n>>\033[0m " % (str(32),label)
        config[key]=rlinput(label,prefill=config[key])
    
    if config.get('jwt','')=='':
        conn=rlinput('Authentication Via : ',prefill='google')
        username=rlinput('Username : ',prefill='')
        password=getpass.getpass('Password : ')
        """
           Programmatic Authentication (Service Accounts)
          A JWT can be obtained authenticating with a user from a Database or AD/LDAP connection by calling the oauth/ro endpoint of the Authentication API, passing a username, password, connection and client_id. This can be used to obtain tokens from any system without user intervention (e.g. scripts, batch files, web backends, native apps). Look under SDK - Authentication API - Database & Active Directory / LDAP Authentication (on the dashboard).
        """       
        raise Exception('not yet implemented')
        
    #d=HAPICLI(config)
    ok=True #d.login()
    if not ok:
        print("Those credentials do not work")
    else:
        save=rlinput('Would you like to save to [Y/N]? ',prefill='Y')
        if save=='Y':
            file=None
            fname=None
            if 'HOME' in os.environ:
                fname="%s/.hapi" % (os.environ['HOME'])
                if fname==None:
                    sys.exit("Missing home directory, can't find $HOME")
                with open(fname,"w") as file:
                    file.write(json.dumps(config, sort_keys=True, indent=4, separators=(',', ': ')))
                    print("Saved config in %s" % fname)
                    
 
