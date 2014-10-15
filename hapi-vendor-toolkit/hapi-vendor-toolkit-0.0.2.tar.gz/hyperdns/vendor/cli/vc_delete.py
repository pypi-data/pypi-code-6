import click,textwrap
from hyperdns.vendor.cli import BaseCommand
from hyperdns.netdns import dotify,RecordSpec

class DeleteCommands(BaseCommand):

    def list_commands(self,ctx):
        return ['zone','resource','record']
            
    @click.command()
    @click.argument('zone_fqdn')
    @click.option('--force','_force',is_flag=True,default=False,
            help="Do not query for zone deletion")
    @click.pass_obj
    def zone(ctx,zone_fqdn,_force):
        """Delete the zone named by zone_fqdn
    
        """
        self=ctx['self']
        zone_fqdn=dotify(zone_fqdn)
        if not _force:
            if not click.confirm('Are you sure you want to delete %s' % zone_fqdn):
                return
                
        self._driver(ctx).deleteZone(zone_fqdn)

    @click.command()
    @click.argument('resource_fqdn')
    @click.option('--force','_force',is_flag=True,default=False,
            help="Do not query for zone deletion")
    @click.pass_obj
    def resource(ctx,resource_fqdn,_force):
        """Delete all records for the resource named by resource_fqdn
    
        """
        self=ctx['self']
        resource_fqdn=dotify(resource_fqdn)
        if not _force:
            if not click.confirm('Are you sure you want to delete %s' % resource_fqdn):
                return
                
        self._driver(ctx).deleteResource(resource_fqdn)

    @click.command()
    @click.argument('fqdn')
    @click.argument('rdtype',type=click.Choice(['A', 'AAAA','CNAME']))
    @click.argument('rdata')
    @click.argument('ttl')
    @click.pass_obj
    def record(ctx,fqdn,rdtype,rdata,ttl):
        """Delete a resource or specific record.  If a value is provided along
        with the FQDN, then only that record is deleted.  If a TTL is provided
        then the record must match both the value and the TTL.

        The type of the record will be guessed from the VALUE, however, this can
        be overridden by passing the --type parameter.
        
        If the resource does not exist then the delete command is ignored.
        """
        
        self=ctx['self']
        driver=self._driver(ctx)
        
        ok,rname,zone_fqdn=driver.validate_rname_in_zone(fqdn)
        if not ok:
            click.echo("Sorry, I could not find a zone matching '%s'" % fqdn)
            return
            
        try:
            spec=RecordSpec(rdata=rdata,rdtype=rdtype,ttl=ttl)
        except Exception as E:
            click.echo("Sorry, can not create record spec from that value: %s" % str(E))
            return
            
        driver.deleteRecord(rname,spec,zone_fqdn=zone_fqdn)
        
        
    def __init__(self,dclass):
        super(DeleteCommands,self).__init__(dclass)
        self.short_help="Delete zones, records, and resources on '%s'" % self.dclass.name
        self.help=textwrap.dedent('''
        Delete zones, records, and resources on '%s'

        Examples:
        
        delete zone <fqdn>
        ''' % self.dclass.name)



