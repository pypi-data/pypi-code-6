import click,json
from .vc_angular import AngularCommands
from .vc_create import CreateCommands
from .vc_delete import DeleteCommands
from hyperdns.vendor.core import import_driver
import textwrap
import hyperdns.vendor.cli
from hyperdns.vendor.cli import PROGNAME
from .vc_test import test as cmd_test
from hyperdns.netdns import (
    dotify,
    is_valid_zone_fqdn,
    RecordType,RecordSpec,
    ZoneData,
    CorruptBindFile
)

class VendorCommands(click.MultiCommand):
    """The set of commands and functions which can run against a vendor
    via the click system.  These are invoked via as `PROG <vkey> <cmd>`
    where vkey determines the scope of the commands.  There is something
    a little bit strange, in that vkey is known at initialization time, so
    a VendorCommands instance is created for each available <vkey>.  However,
    the ctx object is *not* available at that time, so we must pass that in
    during run-time, and this holds the configuration corresponding to the
    vkey.
    """
    def __init__(self,vkey):
        click.MultiCommand.__init__(self)
        
        self.vkey=vkey
        self.dclass=import_driver(vkey)
        if self.dclass==None:
            raise Exception("Failed to load vendor '%s'" % vkey)

        self.short_help="Manage '%s'" % self.dclass.name
        self.help=textwrap.dedent('''
        Complete management of zones, resource, and records for '%s'.  You can
        use this tool to upload and download zonefiles, and to create and delete
        the records in a zone, and so forth.  Unlike HAPI there is no cross-vendor
        support, and you can only interact with a single vendor at a time.
        Consider using HAPI to implement full featured multi-vendor systems, and
        use this for quick interaction with single vendors, and for testing and
        developing drivers.
        ''' % self.dclass.name)

        # load complex subcommands
        self.angular=AngularCommands(self.dclass)   
        self.create=CreateCommands(self.dclass)   
        self.delete=DeleteCommands(self.dclass)   
        self.test=cmd_test
        
        # we create a custom class associated with this vkey to handle the
        # interactive shell.  This is because the do_* methods are introspected
        # at the class level, but the multi-commands above are bound to the
        # instance.  I tried attaching them directly to the class, but ran into
        # trouble since dclass depends upon vkey.  Ideally this stuff (dclass,vkey)
        # would come from the context during the invocation process, but not sure
        # exactly how to do that.
        cname="VendorShell_%s" % (vkey)
        self.shell_class=type(cname,(hyperdns.vendor.cli.VendorShell,),{})
        setattr(self.shell_class,'vkey',vkey)
        shellcmds=['ls','config','upload','download','create','delete','ping']
        for name,docs in [(name,getattr(self,name).help) for name in shellcmds]:
            self._attach_do_method(name,docs)
 

    def _driver(self,ctx,login=False):
        """Return the appropriate driver
        """
        settings=ctx['config']['vendors'].get(self.vkey,None)
        if settings==None:
            raise Exception('Can not obtain driver without credentials')
        return self.dclass(settings,immediateLogin=login)
        

           
    def _attach_do_method(self,name,docs):
        """Attach a do_<cmd> method to the shell class.  This allows cmd.Cmd to
        inpsect the class correctly and to provide services such as interactive
        help.  We implement this as a method instead of in the loop body so that
        the name and docs variables get correctly bound, (otherwise they retain
        the final value from the iteration)
        """
        def do_method(shell,line):
            shell._invoke(name,line)
        do_name='do_%s' % name
        do_method.__name__=do_name
        do_method.__doc__=docs
        setattr(self.shell_class,do_name,do_method)

    # list_commands and get_command are support for click.MultiCommand
    def list_commands(self, ctx):
        """Return the available commands based on what we know about the
        context.  If there is no configuration for the specific vkey, then
        we can only execute config.  If a configuration for a specific vendor
        is available after the configuration has been loaded (e.g. it is in
        ctx.obj), or if ctx.obj==None (indicating that this is being called
        prior to the loading of the config), then we return the full set
        of commands.
        """
        if ctx.obj==None or ctx.obj.get('config',{}).get('vendors',{}).get(self.vkey)!=None:
            return sorted(['shell','ls','config','upload','test','angular',\
                    'download','create','delete','ping'])
        elif ctx.obj.get('config',{}).get(self.vkey)==None:
            return ['config']
        else:
            return []
        
    def get_command(self, ctx, name):
        """Obtain the actual command instance - note that which commands are
        available is sensitive to the status of the ctx and the calling context.
        """
        if name not in self.list_commands(ctx):
            return None
        if name=='shell':
            def run_shell():
                self.shell_class(ctx.obj).cmdloop()
            executor=run_shell
            executor.__name__=name
            helptext=('''
                Run an interactive shell against %s using a single login session
                with the remote vendor.  This uses the python3 cmd.Cmd module but
                it is mapped, mostly against click.  Everything available in the
                shell is available on the command line as
                \b
                >>%s %s <command>
                
                
                However, sometimes you want to process chunks of commands, perhaps
                from some other source, as a batch, using a single login session
                with the remote vendor - and this is the primary use case for the
                shell.
                ''' % (self.dclass.name,PROGNAME,self.dclass.vkey
                )).strip()
            return click.Command(name,callback=executor,help=helptext)
        else:
            ctx.obj['self']=self
            return getattr(self,name)
    
    @click.command()
    @click.pass_context
    def config(ctx):
        """Get the list of settings from the class, get values for each of
        the requested parameters, and ask for each of them.  Then write the
        resulting configuration file.
        """
        vkey=ctx.parent.parent.invoked_subcommand
        dclass=import_driver(vkey)
        
        # the cfile from which our config is loaded
        cfile=ctx.obj.get('cfile')
        
        # our existing configuration, which may or may not contain an actual
        # configuration for this vendor.
        config=ctx.obj.get('config',{})
        vendor_config=config.get('vendors',{})
        settings=vendor_config.setdefault(vkey,{})
        
        # the list of parameters to query
        params=dclass.info.get('settings',[])
        
        # get values
        for p in params:
            settings[p]=click.prompt("%s %s" % (dclass.name,p),
                                            default=settings.get(p,''))

        # save the file out
        with open(cfile,'w+') as openfile:
            click.echo("Writing %s" % cfile)
            openfile.write(json.dumps(config,sort_keys=True,
                          indent=4, separators=(',', ': ')))
        
        ## this feels too hacky, but this is really only viable for mock
        ## drivers, which are the only ones that can use the mock system
        #if hasattr(dclass,'ismock') and getattr(self.dclass,'ismock')==True:
        #        self.dclass._reset_config(self._settings)

                
    @click.command()
    @click.pass_obj
    def ping(ctx,*args,**kwargs):
        """Test that you can log in to the service"""
        self=ctx['self']
        driver=self._driver(ctx,login=False)
        
        try:
            if driver.login():
                click.echo("Login successful")
            else:
                raise Exception("Unable to log in for unknown reason")
        except Exception as E:
            click.echo("Unable to log in: reason=%s" % (E))
        
    @click.command()
    @click.option('--in',type=click.File('r'),default='-',help="file to load, or stdin")
    @click.option('--replace',default=False,is_flag=True,help="should we delete existing zone")
    @click.pass_obj
    def upload(ctx,**kwargs):
        """Upload zone information, either in BIND9 or HyperDNS Zone JSON Format.
        """        
        self=ctx['self']
        input_data=kwargs['in'].read()
        replace=kwargs['replace']
        try:
            jsonobject=json.loads(input_data)
            try:
                zonedata=ZoneData.fromDict(jsonobject)
            except Exception as E:
                click.echo("Syntactically valid, semantically invalid JSON:%s" % E)
                raise
            
        except ValueError as E:
            try:
                zonedata=ZoneData.fromZonefileText(input_data)
            except CorruptBindFile:
                click.echo("I had a problem parsing the bind file")
                return
            except Exception as E:
                click.echo("Failed to process input as either JSON or BIND file:%s" % E)
                return
            
        except Exception as E:
            click.echo("Failed to interpret input:%s" % E)
            return
        
        
        zone_fqdn=zonedata.fqdn
        if not is_valid_zone_fqdn(zone_fqdn):
            click.echo("'%s' is not a valid zone fqdn" % zone_fqdn)
            return
            
        driver=self._driver(ctx,login=True)
            
        if driver.hasZone(zone_fqdn):
            if not replace:
                click.echo("'%s' already exists, use --replace to force deletion" % zone_fqdn)
                return
            else:
                driver.deleteZone(zone_fqdn)
                
        admin_email=zonedata.soa_email
        if admin_email==None:
            admin_email=ctx.get('email')
        default_ttl=zonedata.soa_minimum
        if default_ttl==None:
            default_ttl=ctx.get('default_ttl',800)
            
        click.echo("Creating '%s'" % zone_fqdn)
        driver.createZone(zone_fqdn,admin_email=admin_email,default_ttl=default_ttl)
        for resource in zonedata.resources:
            for record in resource.records:
                if RecordType.as_type(record['type'])==RecordType.SOA:
                    click.echo('Ignoring SOA record, which is created during zone creation')
                else:
                    rname=resource.name
                    # this is a total hack, but until I get the correct semantics
                    # and implementation of the base driver createRecord() method
                    # it'll have to do
                    if record.rdtype in [RecordType.A,RecordType.CNAME]:
                        driver.createRecord(rname,record,zone_fqdn=zone_fqdn)
            

    @click.command()
    @click.argument('zone_fqdn')
    @click.option('--format','output_style',default='json',type=click.Choice(['json', 'bind']))
    @click.option('--out',type=click.File('w'),default='-',help="file to save, or stdout")
    @click.pass_obj
    def download(ctx,zone_fqdn,output_style,out):
        """Download zone information
        
        If format==bind
        Download the BIND9 zonefile for where ZONE_FQDN is a fully qualified (dot-ending)
        name.  However, that dang dot will be added if you don't provide it.
        
        If format==json
        Download the JSON for where ZONE_FQDN is a fully qualified (dot-ending)
                name.  However, that dang dot will be added if you don't provide it.
        """
        self=ctx['self']
        zone_fqdn=dotify(zone_fqdn)
        zone_data=self._driver(ctx).scanZone(zone_fqdn)

        if output_style=='bind':
            zd=ZoneData.fromDict(zone_data)
            bindtext=zd.zonefile
            out.write(bindtext)
        else:
            jsontext=json.dumps(zone_data,sort_keys=True,
                                  indent=4, separators=(',', ': '))
            out.write(jsontext)



    @click.command()
    @click.argument('what',default='')
    @click.pass_obj
    def ls(ctx,what):
        """List zones or list a specific zone or a specific resource.
        
        For example:
        
        ls               will list all of the zones
        ls a.zone        will list the resources in a zone
        ls host.in.zone  will list the records for a resource in a zone
        """
        self=ctx['self']
        driver=self._driver(ctx)
        zl=driver.scanZoneList()
        zonelist=[]
        for z in zl:
            zonelist.append(z['name'])
        zonelist=sorted(zonelist)
        
        if what=='':
            if len(zonelist)==0:
                click.echo("No zones found")
            else:
                for z in zonelist:
                    print(z)
        else:
            fqdn=what
            if not fqdn.endswith("."):
                fqdn=fqdn+"."
            
            # look to see if this fqdn is a zone
            fqdnIsZone=False
            for zname in zonelist:
                if fqdn==zname:
                    fqdnIsZone=True
            
            # list a zone
            if fqdnIsZone:
                zd=driver.scanZone(fqdn)
                if zd==None:
                    print("Not found")
                else:
                    rlist=zd.get('resources',[])
                    if len(rlist)==0:
                        click.echo("Zone %s is empty" % fqdn)
                    else:
                        printset={}
                        maxlen=0
                        for entry in rlist:
                            n=entry['name']
                            if len(n)>maxlen:
                                maxlen=len(n)
                            resolution=[]
                            for rec in [RecordSpec(json=x) for x in entry['records']]:
                                if rec.rdtype in [RecordType.A,RecordType.AAAA,RecordType.CNAME]:
                                    resolution.append('%s,%s' % (rec.rdata,rec.ttl))
                            if len(resolution)==0:
                                resolution=['This resource has no A, AAAA, or CNAME records']
                            printset[n]=resolution
                            
                        fmtstring="%%-%ds:%%s" % maxlen
                        for p in sorted(printset.keys()):
                            print(fmtstring % (p,printset[p]))
                        
            else:
                rname=None
                for zname in zonelist:
                    if fqdn.endswith(zname):
                        rname=fqdn[:-(len(zname)+1)]
                        fqdn=zname
                        break

                if rname==None:
                    print("Not found")
                else:
                    res=driver.scanResource(rname,fqdn)
                    if res==None:
                        print("Resource %s not found in %s" % (rname,fqdn))
                    else:
                        print("Resource %s in %s" % (rname,fqdn))
                        for rec in res.get('records'):
                            rd=rec.get('rdata')
                            ttl=rec.get('ttl')
                            rtype=RecordType.as_str(rec.get('type'))
                            print("  ",rtype,rd,ttl)
        
