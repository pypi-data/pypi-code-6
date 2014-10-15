import click,sys,traceback
from hyperdns.vendor.cli import PROGNAME
from hyperdns.netdns import dotify,RecordSpec,RecordType

class FailureException(Exception):
    pass
    
@click.command()
@click.argument('testzone',default='example.com.',required=False)
@click.option('--force','_force',is_flag=True,default=False,
        help="Do not query for zone deletion")

@click.pass_obj
def test(ctx,testzone,_force):
    """Run a basic sanity check against the vendor.  This will
    create and delete the zone in question, so it will confirm
    that you want to delete that zone before the test executes.
    """
    testzone=dotify(testzone)
    testhost='testhost'
    testfqdn='%s.%s' % (testhost,testzone)

    self=ctx['self']
    driver=self._driver(ctx)
 
    if not _force:
        click.echo("This test will destroy the zone '%s'" % testzone)
        canDelete=click.confirm("Please confirm that you can delete '%s'" % testzone)
    
        if not canDelete:
            click.echo("You can change the zone used by re-invoking the\n"\
                        "command with a different value for testzone.\n"\
                        "For example:\n"\
                        "%s %s test a.new.zone.com" % (PROGNAME,util.vkey))
            return True
    
    try:

        # step #1, erase the zone if it does not exist
        click.echo("Checking to see if %s exists." % testzone)
        if driver.hasZone(testzone):
            click.echo("The zone %s exists, deleting." % testzone)
            driver.deleteZone(testzone)
            
            if driver.hasZone(testzone):
                raise FailureException("Deletion of the zone %s failed." % testzone)
                
        else:
            click.echo("The zone %s does not exist." % testzone)
    
    
        # create the zone
        click.echo("Creating the zone %s" % testzone)
        driver.createZone(testzone,admin_email="zonetest@dnsmaster.io",default_ttl=1234)
        if not driver.hasZone(testzone):
            raise FailureException("Creation of the zone %s failed." % testzone)
    
        # checking scanZoneList - expect to find the zone in the list
        click.echo("Checking that zone %s is visible in scanZoneList." % testzone)
        zl=driver.scanZoneList()
        if not testzone in [z['name'] for z in zl]:
            raise FailureException("scanZoneList does not show the newly created zone %s" % testzone)
        
        # check scan zone
        zd=driver.scanZone(testzone)
        assert zd['name']==testzone
        click.echo("Checking scanZone reports %s is empty except for potential NS and SOA records." % testzone)
        for resource in zd['resources']:
            for r in resource['records']:
                if r.rdtype not in [RecordType.NS,RecordType.SOA]:
                    raise FailureException("Records were found in %s that are not NS or SOA" % testzone)
        
        # now checking that there are no records for the test host
        click.echo("Checking scanResource for host %s" % testhost)
        records=driver.scanResource(testhost,testzone)
        assert records==None
        
        # now checking record creation
        spec=RecordSpec.ipv4_a_record('1.2.3.4',ttl=123)
        assert driver.hasRecord(testfqdn,spec)==False
        driver.createRecord(testfqdn,spec)
        if not driver.hasResource(testfqdn):
            raise FailureException("""
            We created a record on a resource that did not exist, so now the
            resource should exist, but hasResource tells us it does not.
            """)
        assert driver.hasRecord(testfqdn,spec)==True
        
                
        click.echo("Checking that we can delete a resource")
        driver.deleteResource(testfqdn)
        if driver.hasResource(testfqdn):
            raise FailureException("""
                We just deleted a resource, the whole thing, but it seems like
                it is still there.
                """)
        
        
        # reset
        driver.createRecord(testfqdn,spec)
        
        
        
        click.echo("Checking that hasRecord correctly fails to find a record with a different ttl")
        spec=spec.changeTTL(1234)
        if driver.hasRecord(testfqdn,spec):
            raise FailureException("""
                We created a record and used hasRecord() to see if the record
                with a different TTL exists, and hasRecord() said yes.
                """)
        if driver.hasRecord(testfqdn,spec,matchTTL=False)!=True:
            raise FailureException("""
                We created a record, and then checked to see if a record
                with the same values but a different TTL existed - and this
                check failed.  hasRecord() is incorrectly ignoring the
                matchTTL field.
                """)
        
        # this should fail
        driver.deleteRecord(testfqdn,spec)
        assert driver.hasRecord(testfqdn,spec)==False
        assert driver.hasRecord(testfqdn,spec,matchTTL=False)==True
        
        spec=spec.changeTTL(123)
        assert driver.hasRecord(testfqdn,spec)==True
        
        click.echo("Deleting Record - this is the last record, the resource should disappear")
        driver.deleteRecord(testfqdn,spec)
        assert driver.hasRecord(testfqdn,spec)==False
        assert driver.hasRecord(testfqdn,spec,matchTTL=False)==False
        
        click.echo("Checking scanResource for host %s, which should not exist" % testhost)
        info=driver.scanResource(testhost,testzone)
        if info!=None:
            print(info)
            raise FailureException("""
            We have a resource with no records.  This should never exist.  scanResource()
            is reporting that the test host exists, but we have deleted all of it's records.
            """)
        
        spec=RecordSpec.ipv4_a_record('1.2.3.5',spec.ttl)
        driver.createRecord(testfqdn,spec)
        spec=RecordSpec.ipv4_a_record('1.2.3.6',spec.ttl)
        driver.createRecord(testfqdn,spec)
        info=driver.scanResource(testhost,testzone)
        assert len(info['records'])==2
        
        assert driver.hasResource(testhost,testzone)==True
        driver.deleteResource(testfqdn)
        info=driver.scanResource(testhost,testzone)
        assert info==None
        assert driver.hasResource(testhost,testzone)==False

        click.echo("Success! '%s' passed" % driver.name)
    except AssertionError as E:
        _,_,tb = sys.exc_info()
        tbInfo = traceback.extract_tb(tb)
        filename,line,func,text = tbInfo[-1]
        click.echo ('Test Failed - line ' + str(line) + ' in statement ' + text)
    except FailureException as E:
        click.echo("Test failed, %s" % E)
    except Exception as E:
        click.echo("Test failed, %s" % E)
        raise
        
        

#