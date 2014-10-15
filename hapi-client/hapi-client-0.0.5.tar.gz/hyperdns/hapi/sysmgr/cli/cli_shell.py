from hyperdns.hapi.sysmgr.cli import SHAPICLI
import cmd
import sys
from docopt import docopt

def add_command(class_,command,method,hapi):
        def invoke(self,line):
            argv=line.split(" ")
            argv.insert(0,command)
            argv=argv[:-1]
            #print("I AM HERE",argv)
            #print(docopt_doc)
            hapi.arguments=docopt(hapi.docopt_doc,argv=argv)
            hapi.dispatch(command)
            
        mname='do_%s' % command
        invoke.__doc__=method.__doc__
        setattr(class_,mname,invoke)
#
@SHAPICLI.command('Run an interactive shell')
def cmd_shell(arguments,hapi):

    class ZoneShell(cmd.Cmd):
        prompt = ''
        file = None
        zone = None
        
        def do_exit(self,arg):
            """Exit the command line
            """
            return True

        def do_ls(self,arg):
            for r in self.zone.resources:
                print(r)
                
        def do_download(self,arg):
            """Save the zonefile for the current zone.
            """
            
            print("Save zonefile")
            
        def do_upload(self,arg):
            """Load a zonefile for the current zone"""
            print("Load zonefile")
            
        def do_set(self,arg):
            (_rname,_rvalue)=arg.split('=')
            _rname=_rname.strip()
            _rvalue=_rvalue.strip()
            
            r=self.zone.resources.get(_rname)
            if r==None:
                print("Need to create %s.%s" % (_rname,self.zone.fqdn))
            

        def emptyline(self):
            pass
            
        def complete_set(self,text,line,begin_index,end_index):
            return [i for i in self.zone.resources if i.startswith(text)]
                
    class MyInteractive (cmd.Cmd):
        intro = 'Welcome to the SHAPI shell!' \
            + ' (type help for a list of commands.)' \
            + "\n click on the screen to be able to type"
        prompt = 'SHAPI> '
        file = None
            
        def _find_zone(self,arg):
            if not arg.endswith('.'):
                arg=arg+'.'
            z=hapi.zones.get(arg)
            if z==None:
                print("Sorry, couldn't find that %s" % arg)
            return z
                
        def do_exit(self,arg):
            """Exit the command line
            """
            return True

        def do_set(self,arg):
            (_rname,_rvalue)=arg.split('=')
            _rname=_rname.strip()
            if not _rname.endswith('.'):
                _rname=_rname+'.'  
            _rvalue=_rvalue.strip()
            for z,zone in hapi.zones.items():
                if _rname.endswith(z):
                    print("OK")
                    return
            print("Sorry, can not find a matching zone for %s" % (_rname))
            
        def do_ls(self,arg):
            print("Accounts:")
            for z in hapi.accounts:
                print(z)
        
        def emptyline(self):
            pass
            
        def help_security(self):
            print("Provide informaiton about JWT")
            
        def complete_in(self,text,line,begin_index,end_index):
            return [i for i in hapi.zones if i.startswith(text)]
                        
        def do_in(self,arg):
            """Spawn a zone scoped subshell"""
            zone=self._find_zone(arg)
            if zone:
                n=ZoneShell()
                n.prompt='HAPI/%s> ' % (zone.fqdn)
                n.zone=zone
                n.cmdloop()
        
    for command,method in SHAPICLI.command.registry.items():
        if command!='help':
            add_command(MyInteractive,command,method,hapi)

    MyInteractive().cmdloop()
    print("Command loop complete")

