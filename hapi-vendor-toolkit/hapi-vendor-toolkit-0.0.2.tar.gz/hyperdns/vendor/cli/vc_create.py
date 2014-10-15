import click,textwrap
from hyperdns.vendor.core import (
    ZoneAlreadyExistsException,
    RecordAlreadyExistsException
    )
from hyperdns.vendor.cli import BaseCommand
from hyperdns.netdns import (
    dotify,
    RecordSpec,RecordPool,
    CanNotMixARecordsAndCNAMES,
    CanNotMixAAAARecordsAndCNAMES
    )

class CreateCommands(BaseCommand):
    """
    Create zones and records.  Note, you can not create a resource
    without creating a record, so resource creation is implied by creating
    a record for a new resource.
          
    """
    def list_commands(self,ctx):
        return ['zone','record']


            
    @click.command()
    @click.argument('zone_fqdn')
    @click.option('--ttl',default=800,help="Default TTL for the zone")
    @click.option('--email',default=None,help="Admin email for the soa record")
    @click.pass_obj
    def zone(ctx,zone_fqdn,ttl,email):
        """Create an empty zone, where ZONE_FQDN is a fully qualified (dot-ending)
        name.  However, that dang dot will be added if you don't provide it.
    
        If the email is not provided, the email defined in the config will be
        used.  Some vendors do not accept the email value for the SOA record,
        using the value defined internal to their account management system.
        
        Similarly, the default_ttl for the zone can be passed in, but it may or
        may not be accepted by the underlying driver.
        """
        if email==None:
            email=ctx.get('email')
        zone_fqdn=dotify(zone_fqdn)
        try:
            self=ctx['self']
            self._driver(ctx).createZone(zone_fqdn,default_ttl=ttl,admin_email=email)
        except ZoneAlreadyExistsException:
            click.echo("'%s' already exists." % zone_fqdn)

    @click.command()
    @click.argument('fqdn')
    @click.argument('rdtype',type=click.Choice(['A', 'AAAA','CNAME']))
    @click.argument('rdata')
    @click.argument('ttl')
    @click.option('--add','_add',is_flag=True,default=False,
        help="When --add is present, add the record to the the existing set.")
    @click.pass_obj
    def record(ctx,fqdn,rdtype,rdata,ttl,_add):
        """Create a new record with the given value and the given name.
        The FQDN must be in a zone that exists, but the resource itself does
        not need to exist.  For example, if you have created example.com,
        then you can create records for myresource.example.com.  If you have
        not created example.com, then the command will fail.  Use `create zone`
        to create the zone.
        """
        self=ctx['self']
        with self._driver(ctx) as driver:
             
            ok,rname,zone_fqdn=driver.validate_rname_in_zone(fqdn)
            if not ok:
                click.echo("Sorry, I could not find a zone matching '%s'" % fqdn)
                return
            
            try:
                spec=RecordSpec(rdata=rdata,rdtype=rdtype,ttl=ttl)
            except Exception as E:
                click.echo("Sorry, can not create record spec from that value: %s" % str(E))
                return

            resource=driver.scanResource(fqdn)
            if resource!=None:
                pool=RecordPool.from_records(resource['records'])
                try:
                    pool.add(spec)
                except CanNotMixARecordsAndCNAMES:
                    click.echo('You can not mix A records and CNAMES')
                
                    click.echo("Currently this resource has the following records:")
                    index=1
                    for record in pool.records:
                        click.echo("%3d:%5s:%s" % (index,record.rdtype.name,record.rdata))
                        index=index+1
                
                    if click.confirm('Do you want to replace the existing records with this one'):
                        for record in pool.records:
                            click.echo("I am deleting:%s" % spec)
                            driver.deleteRecord(fqdn,record)
                    else:
                        print("No changes have been made")
                        return
            
            
            
        try:
            driver.createRecord(rname,spec,zone_fqdn=zone_fqdn)
        except RecordAlreadyExistsException:
            click.echo("Sorry, this record already exists, can't recreate")
        except Exception as E:
            click.echo("Unable to create this record:%s" % E)
            raise
            
    def __init__(self,dclass):
        super(CreateCommands,self).__init__(dclass)
        self.short_help="Create zones, records, and resources on '%s'" % self.dclass.name
        self.help=textwrap.dedent(self.__doc__)

