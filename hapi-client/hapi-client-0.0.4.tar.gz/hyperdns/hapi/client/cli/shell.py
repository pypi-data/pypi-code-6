import cmd
import sys
import click
from hyperdns.hapi.client.cli import main


@main.command()
@click.pass_obj
def shell(hapi):
    """Interactive HAPI shell.
    
    Example:
        (.python)hapi-client-python3 : hapi shell
        Welcome to the HAPI shell! (type help for a list of commands.)
         click on the screen to be able to type
        HAPI> ls
        zone1.com.
        HAPI> in zone1.com.
        HAPI/zone1.com.> ls
        name1
        name2
        HAPI/zone1.com.> exit
    """
    class BaseShell(cmd.Cmd):
        def do_out(self,arg):
            """Pop up one level
            """
            return True
            
        def do_exit(self,arg):
            """Exit the command line completely
            """
            sys.exit()

        def help_general(self):
            print("""
In general you're probably going to use the following
commands the most:

 ls         list information
 in         change your focus
 change     update dns
 
            """)
            
        def help_security(self):
            print("Provide informaiton about JWT")
            
        def emptyline(self):
            pass
            
        def _find_zone(self,arg):
            if not arg.endswith('.'):
                arg=arg+'.'
            z=hapi.zones.get(arg)
            if z==None:
                print("Sorry, couldn't find that %s" % arg)
            return z

        def _find_resource(self,arg):
            """Take apart arg from right to left, look for a zone
            that matches one of the suffixes
            """
            if arg.endswith("."):
                arg=arg[:-1]
            bits=arg.split(".")
            sofar=""
            while len(bits)>0:
                POP=bits.pop()
                sofar="%s.%s" % (POP,sofar)
                print(sofar)
                zone=hapi.zones.get(sofar)
                if zone!=None:
                    rname=bits.pop()
                    while len(bits)>0:
                        POP=bits.pop()
                        rname="%s.%s" % (POP,rname)
                    print("Yeah:",rname)
            sys.exit()
            
    class ResourceShell(BaseShell):
        prompt = ''
        file = None
        resource = None
        zone = None
    

    class ZoneShell(BaseShell):
        prompt = ''
        file = None
        zone = None
        
        def complete_ls(self,text,line,begin_index,end_index):
            """Returns the completion array for resources"""
            return [i for i in self.zone.resources if i.startswith(text)]

        def do_ls(self,arg):
            """This command takes two forms, without an argument it lists the
            resources.  With an argument it provides detailed information about
            the resource.
            """
            if arg=="":
                for r in self.zone.resources:
                    print(r)
            else:
                resource=self.zone.resources.get(arg)
                if resource==None:
                    print("Resource not found")
                else:
                    print("RESOURCE",resource)
                
        def do_download(self,arg):
            """Save the zonefile for the current zone.
            """
            
            print("Save zonefile")
            
        def do_upload(self,arg):
            """Load a zonefile for the current zone"""
            print("Load zonefile")
            
        def do_change(self,arg):
            """
            """
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
                
    class MyInteractive (BaseShell):
        intro = 'Welcome to the HAPI shell!' \
            + ' (type help for a list of commands.)' \
            + "\n click on the screen to be able to type"
        prompt = 'HAPI> '
        file = None
            

        def _recspec_from_line(self,arg):
            argparts=arg.split(" ")
            if len(argparts)!=4:
                print("Malformed record spec")
                return None
            
            (_fqdn,_rdtype,_rdata,_ttl)=argparts
            return None

        def do_addrec(self,arg):
            """
            Assert a record - e.g. addrec <fqdn> <type> <value> <ttl>

            This is the 'no frills' version of add.  This requires
            that <fqdn> point to a specific resource in an existing zone.  The
            resource does not need to exist, but the zone does.  If the resource
            does not exist, it will be created.  The record will be added to
            the existing pool of records as follows:
                 A and AAAA
                     These records will have the value added if it is new, but
                     if the value already exists only the ttl will be updated.
                 singletons
                     These records will be overwritten
                 other
                     The record will be added to the resource record pool.
        
            Example Invocations:
                addrec <fqdn> <type> <value> <ttl>
            """
            recspec=self._recspec_from_line(arg)
            if recspec==None:
                return
                
                
        def do_delrec(self,arg):
            """
            Delete a record
            
            This is the 'no frills' version of delete.  This requires that you
            specify the record exactly - there is no assistive matching, and if
            you don't get a value right we'll just bork the input.
    
            Example Invocations:
                delrec <fqdn> <type> <value> <ttl>
            """
            recspec=self._recspec_from_line(arg)
            if recspec==None:
                return
                


        def do_delete(self,arg):
            """
            Delete zones, resource, and records
            
            Example Invocations:
                delete <zone>
                delete <resource>.<zone>
                delete <value> from <resource>.<zone>
            """
            if arg=="":
                print("Summary deletion is a bad idea")
                return
                
            

        def do_change(self,arg):
            """Change your DNS
            
            Example Invocations:
                change <resource>.<zone> to <value>
                change <resource>.<zone> to <value> ttl <ttl>
                change <resource>.<zone> add <ip|ipv6>
                change <resource>.<zone> ttl <ttl>
            """
            if arg=="":
                print("Change is good")
                return
            
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





        def complete_ls(self,text,line,begin_index,end_index):
            return ["zones","vendors"]
            
        def _ls_list_zones(self):
            """List the zones
            """
            for z in hapi.zones:
                print(z)
                
        def _ls_list_vendors(self):
            """List the vendors
            """
            for v in hapi.vendors:
                print(v)
                
        def _ls_list_users(self):
            """List the user
            """
            for z in hapi.admin:
                print(z)
                
            
        def do_ls(self,arg):
            """List information about the current environment.
            
            Example Invocations:
                ls
                ls zones
                    by itself, ls lists the zones
                ls vendors
                    list the configured vendors
                ls <fqdn>
            """
            if arg=="zones" or arg=="":
                self._ls_list_zones()
            elif arg=="vendors":
                self._ls_list_vendors()
            else:
                # look for a zone or a resource
                print("look for")
        





        def complete_in(self,text,line,begin_index,end_index):
            return [i for i in hapi.zones if i.startswith(text)]
                        
        def do_in(self,arg):
            """
            Spawn a zone or a resource scoped subshell.
            
            Example Invocations
                in zone1.com
                in host.zone1.com
            """
            zone=self._find_zone(arg)
            if zone:
                n=ZoneShell()
                n.prompt='HAPI/%s> ' % (zone.fqdn)
                n.zone=zone
                n.cmdloop()
            else:
                (resource,zone)=self._find_resource(arg)
                if resource:
                    r=ResourceShell()
                    r.zone=zone
                    r.resource=resource
                    r.prompt='HAPI/%s.%s> ' % (resource.name,zone.fqdn)
                    r.cmdloop()

    MyInteractive().cmdloop()
    print("Have a HAPI day")

